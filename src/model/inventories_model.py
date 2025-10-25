import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.config import get_connection
from src.dto.inventory_dto import InventoryDTO, InventoryLogDTO
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
 
    
class InventoryLog_model():
    @staticmethod
    def create_log(log: InventoryLogDTO):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                insert into Inventory_Logs (ProductID, UserID, Quantity, DateChange)
                OUTPUT INSERTED.LogID
                values (?,?,?,?)
            """
            cursor.execute(query, (log.ProductID, log.UserID, log.Quantity, datetime.now()))
            new_id = cursor.fetchone()[0] 
            conn.commit()
            return new_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
