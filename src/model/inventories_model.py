import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.config import get_connection
from src.dto.inventory_dto import InventoryDTO, InventoryLogDTO, InventoryLog_full
from datetime import datetime

class Inventories_model():
    @staticmethod
    def create_inventory(inventory: InventoryDTO):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO Inventories (ProductID, Quantity)
                OUTPUT INSERTED.InventoryID
                values (?,?)
            """
            cursor.execute(query, (inventory.ProductID,inventory.Quantity))
            new_id = cursor.fetchone()[0] 
            conn.commit()
            return new_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_inventory_byProductID(id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Inventories WHERE ProductID = ?", (id,))
            row = cursor.fetchone()
            if row:
                inventory = InventoryDTO(
                    ProductID= row[1],
                    Quantity= row[3]
                )
                return inventory
            return None

        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_all_inventories(Page: int = 1):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            page_size = 20
            offset = (Page - 1) * page_size

            query = """
                SELECT * 
                FROM Inventories
                ORDER BY ProductID
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
            """

            cursor.execute(query, (offset, page_size))
            rows = cursor.fetchall()
            inventories = []

            for row in rows:
                # ⚠️ Điều chỉnh thứ tự cột theo đúng cấu trúc bảng của bạn
                inventory = InventoryDTO(
                    ProductID=row[1],
                    Quantity=row[3]
                )
                inventories.append(inventory)

            return inventories

        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def restock(product: InventoryDTO, log: InventoryLog_full):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.autocommit = False  # Bắt đầu transaction

            # 1️⃣ Kiểm tra tồn kho hiện tại
            existing_inventory = Inventories_model.get_inventory_byProductID(product.ProductID)

            if existing_inventory:
                # 2️⃣ Nếu đã có thì cộng thêm vào số lượng hiện tại
                new_quantity = existing_inventory.Quantity + product.Quantity
                update_query = """
                    UPDATE Inventories
                    SET Quantity = ?
                    WHERE ProductID = ?
                """
                cursor.execute(update_query, (new_quantity, product.ProductID))
            else:
                # 3️⃣ Nếu chưa có thì tạo mới
                insert_query = """
                    INSERT INTO Inventories (ProductID, Quantity)
                    VALUES (?, ?)
                """
                cursor.execute(insert_query, (product.ProductID, product.Quantity))

            # 4️⃣ Ghi log vào Inventory_Logs
            log_query = """
                INSERT INTO Inventory_Logs (ProductID, ProductName, UserID, UserName, Quantity, DateChange)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(log_query, (
                log.ProductID,
                log.ProductName,
                log.UserID,
                log.UserName,
                log.Quantity,
                datetime.now()
            ))

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
 
