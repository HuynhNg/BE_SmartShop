import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.config import get_connection
from src.dto.user_dto import LoginDTO, RegisterDTO, UserDTO


class Users_model:
    @staticmethod
    def get_all_users(page: int):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM Users u
                ORDER BY u.UserID
                OFFSET ? ROWS FETCH NEXT 20 ROWS ONLY        
            """, ((page - 1) * 20,))

            rows = cursor.fetchall()
            users = [
                UserDTO(
                    UserID=int(row[0]),
                    UserName=row[1],
                    PhoneNumber=row[2],
                    Address=row[3],
                    Email=row[4],
                    Password=row[5],
                    RoleID=int(row[6])
                )
                for row in rows
            ]
            return users

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_user_byID(UserID: int):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM Users u
                WHERE UserID = ?
            """, (UserID,))

            row = cursor.fetchone()
            if row:
                return UserDTO(
                    UserID=int(row[0]),
                    UserName=row[1],
                    PhoneNumber=row[2],
                    Address=row[3],
                    Email=row[4],
                    Password=row[5],
                    RoleID=int(row[6])
                )
            return None

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_user_byEmail(Email: str):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM Users u
                WHERE Email = ?
            """, (Email,))

            row = cursor.fetchone()
            if row:
                return UserDTO(
                    UserID=int(row[0]),
                    UserName=row[1],
                    PhoneNumber=row[2],
                    Address=row[3],
                    Email=row[4],
                    Password=row[5],
                    RoleID=int(row[6])
                )
            return None

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def login(user: LoginDTO):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT UserID, RoleID
                FROM Users
                WHERE Email = ? AND Password = ?
            """
            cursor.execute(query, (user.Email, user.Password))
            row = cursor.fetchone()
            if row:
                return row[0], row[1]
            return None, None

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def register(user: RegisterDTO, RoleID: int):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO Users (UserName, PhoneNumber, Address, Email, Password, RoleID)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (user.UserName, user.PhoneNumber, user.Address, user.Email, user.Password, RoleID))
            conn.commit()

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    @staticmethod
    def update_user(user_id: int, user : RegisterDTO):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            conn.autocommit = False  
            cursor = conn.cursor()
            old_user = Users_model.get_user_byID(user_id)

            query = """
                Update Users
                Set UserName = ?, PhoneNumber = ?, Address = ?, Email = ?, Password = ?
                where UserID = ?
            """
            cursor.execute(query, (user.UserName, user.PhoneNumber, user.Address, user.Email, user.Password, user_id))
            
            if old_user.UserName != user.UserName:
                query_update_order = """
                    Update Orders
                    Set UserName = ?
                    where UserID = ? and UserName = ?
                """

                query_update_log = """
                    Update Inventory_Logs
                    Set UserName = ?
                    where UserID = ? and UserName = ?
                """
                cursor.execute(query_update_order, (user.UserName, user_id, old_user.UserName))
                cursor.execute(query_update_log, (user.UserName, user_id, old_user.UserName))
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
