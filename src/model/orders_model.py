import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.config import get_connection
from datetime import datetime
from src.dto.order_dto import Order, OrderDetail, NewOrder
from src.dto.product_dto import ProductOrder
from typing import List
from src.model.inventories_model import Inventories_model


class Orders_model:
    @staticmethod
    def get_all_orders(Page: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            page_size = 20
            offset = (Page - 1) * page_size

            query = """
                SELECT * 
                FROM Orders
                ORDER BY OrderDate DESC
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
            """

            cursor.execute(query, (offset, page_size))
            rows = cursor.fetchall()

            orders = [
                Order(
                    OrderID=row[0],
                    UserID=row[1],
                    UserName=row[2],
                    Address=row[3],
                    PhoneNumber=row[4],
                    Price=row[5],
                    OrderDate=row[6],
                )
                for row in rows
            ]

            return orders

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_order_byID(OrderID: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT OrderID, UserID, UserName, Address, PhoneNumber, Price, OrderDate
                FROM Orders
                WHERE OrderID = ?
            """

            cursor.execute(query, (OrderID,))
            row = cursor.fetchone()

            if not row:
                return None

            return Order(
                OrderID=row[0],
                UserID=row[1],
                UserName=row[2],
                Address=row[3],
                PhoneNumber=row[4],
                Price=row[5],
                OrderDate=row[6],
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_order_detail(OrderID: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT OrderDetailID, OrderID, ProductID, ProductName, Quantity, Unit_price
                FROM Order_Details
                WHERE OrderID = ?
            """

            cursor.execute(query, (OrderID,))
            rows = cursor.fetchall()

            return [
                OrderDetail(
                    OrderDetailID=row[0],
                    OrderID=row[1],
                    ProductID=row[2],
                    ProductName=row[3],
                    Quantity=row[4],
                    Unit_price=row[5],
                )
                for row in rows
            ]

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def create_order(user_id: int, new_order: NewOrder, product_list: List[ProductOrder]):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.autocommit = False

            insert_order_query = """
                INSERT INTO Orders (UserID, UserName, Address, PhoneNumber, Price, OrderDate)
                OUTPUT INSERTED.OrderID
                VALUES (?, ?, ?, ?, ?, ?)
            """
            total_price = sum(item.Quantity * item.Unit_price for item in product_list)
            order_date = datetime.now()

            cursor.execute(
                insert_order_query,
                (
                    user_id,
                    new_order.UserName,
                    new_order.Address,
                    new_order.PhoneNumber,
                    total_price,
                    order_date,
                ),
            )
            order_id = cursor.fetchone()[0]

            # map tồn kho
            inventory_map = {
                item.ProductID: Inventories_model.get_inventory_byProductID(item.ProductID).Quantity
                for item in product_list
            }

            insert_detail_query = """
                INSERT INTO Order_Details (OrderID, ProductID, ProductName, Quantity, Unit_price)
                VALUES (?, ?, ?, ?, ?)
            """

            update_inventory_query = """
                UPDATE Inventories SET Quantity = ? WHERE ProductID = ?
            """

            insert_log_query = """
                INSERT INTO Inventory_Logs (ProductID, ProductName, UserID, UserName, Quantity, DateChange)
                VALUES (?, ?, ?, ?, ?, ?)
            """

            for item in product_list:
                cursor.execute(
                    insert_detail_query,
                    (order_id, item.ProductID, item.ProductName, item.Quantity, item.Unit_price),
                )

                new_quantity = inventory_map[item.ProductID] - item.Quantity
                cursor.execute(update_inventory_query, (new_quantity, item.ProductID))

                cursor.execute(
                    insert_log_query,
                    (
                        item.ProductID,
                        item.ProductName,
                        user_id,
                        new_order.UserName,
                        -item.Quantity,
                        order_date,
                    ),
                )

            conn.commit()
            return order_id

        except Exception:
            conn.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def delete_order(order_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.autocommit = False

            order = Orders_model.get_order_byID(order_id)

            order_details = Orders_model.get_order_detail(order_id)

            update_inventory_query = """
                UPDATE Inventories SET Quantity = ? WHERE ProductID = ?
            """
            insert_log_query = """
                INSERT INTO Inventory_Logs (ProductID, ProductName, UserID, UserName, Quantity, DateChange)
                VALUES (?, ?, ?, ?, ?, ?)
            """

            now = datetime.now()

            for item in order_details:
                inventory = Inventories_model.get_inventory_byProductID(item.ProductID)
                if not inventory:
                    raise Exception(f"Inventory not found for ProductID {item.ProductID}")

                new_quantity = inventory.Quantity + item.Quantity
                cursor.execute(update_inventory_query, (new_quantity, item.ProductID))

                cursor.execute(
                    insert_log_query,
                    (
                        item.ProductID,
                        item.ProductName,
                        getattr(order, "UserID", None),
                        getattr(order, "UserName", None),
                        item.Quantity,
                        now,
                    ),
                )

            cursor.execute("DELETE FROM Orders WHERE OrderID = ?", (order_id,))
            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
