from dotenv import load_dotenv
import os
import pyodbc

load_dotenv()

DB_SERVER = os.getenv("DATABASE_SERVER", "localhost")
DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER", "sa")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_PORT = os.getenv("DATABASE_PORT", "1433")

def get_connection():
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        f"Server={DB_SERVER},{DB_PORT};"
        f"Database={DB_NAME};"
        f"Uid={DB_USER};"
        f"Pwd={DB_PASSWORD};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    try:
        conn = pyodbc.connect(conn_str)
        print(f"✅ Connected to SQL Server: {DB_SERVER}")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to SQL Server: {e}")
        raise e
