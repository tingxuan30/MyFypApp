
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# SQL Server Configuration
SERVER = r"LAPTOP-O1QC06UC\SQLEXPRESS01"
DATABASE = "VegPriceMYDB"

def get_engine():

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    connection_url = URL.create(
        "mssql+pyodbc",
        query={
            "odbc_connect": connection_string
        }
    )

    engine = create_engine(connection_url)

    return engine

def get_connection():

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    connection = pyodbc.connect(connection_string)

    return connection


def test_database():

    connection = get_connection()

    cursor = connection.cursor()

    print("Connected to VegPriceMYDB!")
    print("\nChecking database tables...\n")

    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)

    tables = cursor.fetchall()

    for table in tables:
        print(table[0])

    cursor.close()
    connection.close()


def check_table_columns(table_name):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COLUMN_NAME,
            DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
    """

    cursor.execute(query, table_name)

    columns = cursor.fetchall()

    print(f"\nTable: {table_name}")
    print("-" * 50)

    for column in columns:
        print(f"{column[0]} : {column[1]}")

    cursor.close()
    connection.close()


if __name__ == "__main__":

    try:
        test_database()

        check_table_columns("2025PriceCatcherRaw")
        check_table_columns("lookup_item")
        check_table_columns("lookup_premise")

    except Exception as e:
        print("Database error:")
        print(e)
