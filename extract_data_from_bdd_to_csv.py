import pyodbc
import os
import pandas as pd
from dotenv import load_dotenv


def connect_to_database():
    """Establish database connection using environment variables"""
    load_dotenv()  # Load environment variables from .env file
    
    # Construct connection string
    SERVER = os.getenv("SERVER")
    DATABASE = os.getenv("DATABASE")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    
    connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    
    try:
        # Establish connection
        cnxn = pyodbc.connect(connection_string)
        return cnxn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_filtered_table(connection):
    """Retrieve filtered table data from the database"""
    try:
        cursor = connection.cursor()
        sql_query = """
        SELECT TABLE_SCHEMA + '.' + TABLE_NAME AS full_table_name 
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA IN ('Person', 'Production', 'Sales')"""
        
        cursor.execute(sql_query)
        table_name = cursor.fetchall()
        table_name = [row[0] for row in table_name]
        print(table_name)
        return table_name
    except pyodbc.Error as e:
        print(f"Error executing SQL query in get_filtered_table : {e}")
        return None
    
def extract_data_to_csv(table_name, connection, output_dir='exported_data'):
    """Extract data from the specified table and save it to a CSV file"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Read entire table
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, connection)
        
        # Generate safe filename
        safe_filename = table_name.replace('.', '_') + '.csv'
        file_path = os.path.join(output_dir, safe_filename)
        
        # Export to CSV
        df.to_csv(file_path, index=False)
        print(f"Exported {table_name} to {file_path}")
    except Exception as e:
        print(f"Error exporting {table_name}: {e}")


def main():
    # Connect to database 
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        # get filtered tables
        tables = get_filtered_table(connection)

        for table in tables:
            extract_data_to_csv(table, connection)
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        # Close connection
        connection.close()

if __name__ == "__main__":
    main()