import pyodbc
import random
from faker import Faker
from tqdm import tqdm
from config import get_connection
from datetime import datetime

# --- Kết nối ---
conn = get_connection()
cursor = conn.cursor()

faker = Faker('vi_VN')

# =========================
# Roles
# =========================
print("Inserting Roles...")
roles = [
    ("Admin", "System administrator"),
    ("Customer", "Regular customer")
]
cursor.executemany(
    "INSERT INTO Roles (RoleName, Description) VALUES (?, ?)",
    roles
)
conn.commit()

# =========================
# Users
# =========================
def generate_phone():
    prefixes = ["03", "05", "07", "08", "09"]
    return f"{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

print("Inserting Users...")

user_query = """
    INSERT INTO Users (UserName, PhoneNumber, Address, Email, Password, RoleID)
    VALUES (?, ?, ?, ?, ?, ?)
"""

# Admin
cursor.execute(user_query, (
    "Admin User",
    generate_phone(),
    faker.address(),
    "admin@smartshop.com",
    "12345678",
    1
))

# 100 Customers
user_data = []
for _ in range(100):
    user_data.append((
        faker.name(),
        generate_phone(),
        faker.address(),
        faker.unique.email(),
        "12345678",
        2
    ))
cursor.executemany(user_query, user_data)
conn.commit()

# Lấy danh sách Users để tạo Inventory_Logs/Orders snapshot
cursor.execute("SELECT UserID, UserName, Email, PhoneNumber, Address FROM Users")
users = cursor.fetchall()
user_dict = {u.UserID: {"UserName": u.UserName, "Email": u.Email, "PhoneNumber": u.PhoneNumber, "Address": u.Address} for u in users}

# =========================
# Categories
# =========================
print("Inserting Categories...")
category_data = [(f"Category {i+1}", faker.sentence(nb_words=5)) for i in range(100)]
cursor.executemany(
    "INSERT INTO Categories (CategoryName, Description) VALUES (?, ?)",
    category_data
)
conn.commit()

# Lấy danh sách Categories
cursor.execute("SELECT CategoryID FROM Categories")
categories = [c.CategoryID for c in cursor.fetchall()]

# =========================
# Products
# =========================
print("Inserting Products...")
product_data = []
num_products = 10000

for i in range(num_products):
    category_id = random.choice(categories)
    product_name = f"Product {i+1}"
    price = random.randint(10, 200) * 1000  # BIGINT VND
    is_active = random.randint(0, 1)
    product_data.append((product_name, price, category_id, is_active))

cursor.executemany("""
    INSERT INTO Products (ProductName, Price, CategoryID, isActive)
    VALUES (?, ?, ?, ?)
""", product_data)
conn.commit()

# Lấy danh sách Products để snapshot
cursor.execute("SELECT ProductID, ProductName FROM Products")
products = cursor.fetchall()
product_dict = {p.ProductID: p.ProductName for p in products}

# =========================
# Inventories & Inventory_Logs
# =========================
print("Inserting Inventories and Inventory Logs...")
inventory_data = []
inventory_logs = []

admin_user = user_dict[1]  # Admin UserID=1

for product in tqdm(products):
    product_id = product.ProductID
    product_name = product.ProductName
    quantity = random.randint(0, 100)

    # Inventory
    inventory_data.append((product_id, product_name, quantity))

    # Inventory Logs - chỉ Admin thực hiện nhập hàng
    if quantity > 0:
        inventory_logs.append((
            product_id,
            product_name,
            1,  # UserID=1 (Admin)
            admin_user["UserName"],
            admin_user["Email"],
            quantity,
            datetime.now()
        ))

cursor.executemany("""
    INSERT INTO Inventories (ProductID, ProductName, Quantity)
    VALUES (?, ?, ?)
""", inventory_data)

cursor.executemany("""
    INSERT INTO Inventory_Logs (ProductID, ProductName, UserID, UserName, Email, Quantity, DateChange)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", inventory_logs)
conn.commit()

# # =========================
# # Orders & Order_Details
# # =========================
# print("Inserting Orders and Order Details...")
# order_data = []
# order_details_data = []

# num_orders = 5000

# for _ in tqdm(range(num_orders)):
#     # Random User
#     user = random.choice(users)
#     order_price = 0

#     # Tạo Order
#     order_data.append((
#         user.UserID,
#         user.UserName,
#         user.Address,
#         user.PhoneNumber,
#         0,  # tạm thời, sẽ update sau
#         datetime.now()
#     ))

# cursor.executemany("""
#     INSERT INTO Orders (UserID, UserName, Address, PhoneNumber, Price, OrderDate)
#     VALUES (?, ?, ?, ?, ?, ?)
# """, order_data)
# conn.commit()

# # Lấy OrderID vừa insert
# cursor.execute("SELECT OrderID, UserID FROM Orders")
# orders = cursor.fetchall()

# # Tạo Order Details
# for order in tqdm(orders):
#     order_id = order.OrderID
#     num_items = random.randint(1, 5)
#     total_price = 0

#     products_sample = random.sample(products, num_items)
#     for product in products_sample:
#         product_id = product.ProductID
#         product_name = product.ProductName
#         quantity = random.randint(1, 10)
#         unit_price = random.randint(10, 200) * 1000
#         total_price += quantity * unit_price

#         order_details_data.append((
#             order_id,
#             product_id,
#             product_name,
#             quantity,
#             unit_price
#         ))

#     # Update Order Price
#     cursor.execute("UPDATE Orders SET Price=? WHERE OrderID=?", (total_price, order_id))

# cursor.executemany("""
#     INSERT INTO Order_Details (OrderID, ProductID, ProductName, Quantity, Unit_price)
#     VALUES (?, ?, ?, ?, ?)
# """, order_details_data)
# conn.commit()

print("✅ Done inserting all fake data!")

cursor.close()
conn.close()
