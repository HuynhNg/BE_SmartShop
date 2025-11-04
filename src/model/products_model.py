import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.config import get_connection
from src.dto.product_dto import ProductResponseDTO
from src.dto.product_dto import ProductCreateDTO, Product
from datetime import datetime

class Products_model():
    @staticmethod
    def get_all_products(page: int, size: int = 20, sort_order: int = None):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            start = (page - 1) * size

            # Xác định hướng sắp xếp theo yêu cầu
            if sort_order == 1:
                order_clause = "ORDER BY p.isActive ASC"
            elif sort_order == 2:
                order_clause = "ORDER BY p.ProductID"  
            else:
                order_clause = "ORDER BY p.isActive DESC"

            # Ghép câu truy vấn
            query = f"""
                SELECT 
                    p.ProductID, 
                    p.ProductName, 
                    c.CategoryName, 
                    p.Price, 
                    p.isActive
                FROM Products p
                JOIN Categories c ON p.CategoryID = c.CategoryID
                {order_clause}
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
            """

            cursor.execute(query, (start, size))
            rows = cursor.fetchall()

            products = [
                ProductResponseDTO(
                    ProductID=row[0],
                    ProductName=row[1],
                    Category=row[2],
                    Price=int(row[3]),
                    isActive=bool(row[4])
                )
                for row in rows
            ]

            return products

        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def get_product_byID(ProductID: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    p.ProductID, 
                    p.ProductName, 
                    c.CategoryName, 
                    p.Price, 
                    p.isActive
                FROM Products p
                JOIN Categories c ON p.CategoryID = c.CategoryID
                where ProductID =?
            """, ((ProductID,)))

            rows = cursor.fetchall()
            if rows:
                product = ProductResponseDTO(
                    ProductID=rows[0][0],
                    ProductName=rows[0][1],
                    Category=rows[0][2],
                    Price=int(rows[0][3]),
                    isActive=bool(rows[0][4]))
                return product
            return None
        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def create_product(Product: ProductCreateDTO):
        """
        Tạo sản phẩm mới:
        - Thêm vào Products
        - Thêm vào Inventories (snapshot ProductName)
        - Thêm Inventory_Logs (snapshot ProductName, UserName, Email)
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.autocommit = False  

            # --- 1. Insert Product ---
            query = """
                INSERT INTO Products (ProductName, Price, CategoryID, isActive)
                OUTPUT INSERTED.ProductID, INSERTED.ProductName
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (Product.ProductName, Product.Price, Product.CategoryID, 1))
            row = cursor.fetchone()
            new_id = row.ProductID
            product_name_snapshot = row.ProductName

            # --- 2. Insert Inventory ---
            query = """
                INSERT INTO Inventories (ProductID, ProductName, Quantity)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (new_id, product_name_snapshot, Product.Quantity))

            # --- 3. Insert Inventory_Log ---
            query = """
                INSERT INTO Inventory_Logs (ProductID, ProductName, UserID, UserName, Email, Quantity, DateChange)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(
                query,
                (
                    new_id,
                    product_name_snapshot,
                    Product.UserID,
                    Product.UserName,    # snapshot
                    Product.Email,   # snapshot
                    Product.Quantity,
                    datetime.now()
                )
            )

            conn.commit()
            return new_id

        except Exception as e:
            if conn:
                conn.rollback()
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def update_product(Product: Product, check_newName: int = 0):
        """
        Cập nhật sản phẩm:
        - Cập nhật Products
        - Cập nhật ProductName trong Inventories
        - Cập nhật ProductName trong Inventory_Logs (nếu muốn overwrite snapshot)
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            conn.autocommit = False
            cursor = conn.cursor()

            # 1. Update Products
            cursor.execute("""
                UPDATE Products
                SET ProductName = ?, Price = ?, CategoryID = ?, isActive = ?
                WHERE ProductID = ?
            """, (Product.ProductName, Product.Price, Product.CategoryID, int(Product.isActive), Product.ProductID))

            if check_newName:
                # 2. Update Inventories snapshot
                cursor.execute("""
                    UPDATE Inventories
                    SET ProductName = ?
                    WHERE ProductID = ?
                """, (Product.ProductName, Product.ProductID))

                # 3. Update Inventory_Logs snapshot (cẩn thận nếu muốn giữ lịch sử, có thể bỏ bước này)
                cursor.execute("""
                    UPDATE Inventory_Logs
                    SET ProductName = ?
                    WHERE ProductID = ?
                """, (Product.ProductName, Product.ProductID))

            conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def delete_product(id: int):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            conn.autocommit = False 
            cursor = conn.cursor()

            query = """
                DELETE FROM Products
                WHERE ProductID = ?
            """
            cursor.execute(query, (id,))
            conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()