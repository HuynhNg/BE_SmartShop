import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.config import get_connection
from src.dto.category_dto import Category, CategoryCreateDTO
from src.dto.product_dto import Product

class Categories_model():
    @staticmethod
    def get_all_categories():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                select * 
                from Categories
            """)

            rows = cursor.fetchall()
            Categories = []

            for row in rows:
                category = Category(
                    CategoryID= row[0],
                    CategoryName= row[1],
                    Description= row[2]
                )
                Categories.append(category)

            return Categories
        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def get_category_byID(CategoryID: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                select * 
                from Categories
                where CategoryID = ?
            """, (CategoryID,))

            rows = cursor.fetchall()
            if rows:
                category = Category(
                    CategoryID= rows[0][0],
                    CategoryName= rows[0][1],
                    Description= rows[0][2]
                )

                return category
            return None
        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_all_products_byCategoryID(CategoryID: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                select * 
                from Products
                where CategoryID = ?
            """, (CategoryID,))

            rows = cursor.fetchall()
            products = []
            for row in rows:
                product = Product(
                    ProductID=row[0],
                    ProductName=row[1],
                    Price=int(row[2]),
                    CategoryID=row[3],
                    isActive= bool(row[4])
                )
                products.append(product)
            
            return products
        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def create_category(category: CategoryCreateDTO):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.autocommit = False  
            query = """
                INSERT INTO Categories (CategoryName, Description)
                OUTPUT INSERTED.CategoryID
                VALUES (?, ?)
            """
            cursor.execute(query, (category.CategoryName, category.Description))
            row = cursor.fetchone()
            new_id = row.CategoryID
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
    def update_category(CategoryID,category: CategoryCreateDTO):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.autocommit = False  
            query = """
                Update Categories
                Set CategoryName =? , Description = ?
                where CategoryID = ?
            """
            cursor.execute(query, (category.CategoryName, category.Description, CategoryID))
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
    def delete_category(CategoryID: int):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            conn.autocommit = False 
            cursor = conn.cursor()

            query = """
                DELETE FROM Categories
                WHERE CategoryID = ?
            """
            cursor.execute(query, (CategoryID,))
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