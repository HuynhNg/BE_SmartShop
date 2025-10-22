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

# --- Roles ---
print("Inserting Roles...")
roles = [
    ("Admin", "System administrator"),
    ("Customer", "Regular customer")
]
for name, description in roles:
    cursor.execute(
        "INSERT INTO Roles (RoleName, Description) VALUES (?, ?)",
        (name, description)
    )
conn.commit()

def generate_phone():
    prefixes = ["03", "05", "07", "08", "09"]
    return f"{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

# --- Users ---
print("Inserting Users...")
query = """
    INSERT INTO Users (UserName, PhoneNumber, Address, Email, Password, RoleID)
    VALUES (?, ?, ?, ?, ?, ?)
"""

# Admin
cursor.execute(query, (
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

cursor.executemany(query, user_data)
conn.commit()

# --- Categories ---
print("Inserting Categories...")
category_data = [(f"Category {i+1}", faker.sentence(nb_words=5)) for i in range(100)]
cursor.executemany(
    "INSERT INTO Categories (CategoryName, Description) VALUES (?, ?)",
    category_data
)
conn.commit()

# --- Products ---
print("Inserting Products...")
product_data = []
for i in range(10000):
    product_data.append((
        random.randint(1, 100),
        f"Product {i+1}",
        random.randint(10, 200) * 1000,
        random.randint(0, 1)
    ))

cursor.executemany("""
    INSERT INTO Products (CategoryID, ProductName, Price, isActive)
    VALUES (?, ?, ?, ?)
""", product_data)
conn.commit()

# --- Inventories & Inventory_Logs---
print("Inserting Inventories...")
inventory_data = []
inventory_logs = []

for i in range(10000):
    productID = i + 1
    quantity = random.randint(0, 100)
    inventory_data.append((productID, quantity))
    if quantity > 0:
        inventory_logs.append((productID, 2, quantity, datetime.now()))

cursor.executemany(
    "INSERT INTO Inventories (ProductID, Quantity) VALUES (?, ?)",
    inventory_data
)

cursor.executemany(
    "INSERT INTO Inventory_Logs (ProductID, UserID, Quantity, DateChange) VALUES (?, ?, ?, ?)",
    inventory_logs
)
conn.commit()

print("✅ Done inserting all fake data!")

cursor.close()
conn.close()
