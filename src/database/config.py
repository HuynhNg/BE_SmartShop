from dotenv import load_dotenv
import os
import pyodbc

load_dotenv()

DB_server = os.getenv("database_server")
DB_name = os.getenv("database_name")
DB_user = os.getenv("database_user")
DB_password = os.getenv("database_password")

def get_connection():
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={DB_server};"
        f"Database={DB_name};"
        f"UID={DB_user};"
        f"PWD={DB_password};"
    )
    try:
        conn = pyodbc.connect(conn_str)
        print("Database connection established.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e
    
conn = get_connection()