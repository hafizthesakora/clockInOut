# import os
# import sqlite3
# import pandas as pd

# def create_employees_table(conn):
#     cur = conn.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS EmployeesData (FullName text PRIMARY KEY)")
#     conn.commit()

# def insert_data_unique(conn, data, table_name):
#     cursor = conn.cursor()
#     for _, row in data.iterrows():
#         try:
#             cursor.execute(f"INSERT OR IGNORE INTO {table_name} (FullName) VALUES (?)", (row['FullName'],))
#         except sqlite3.IntegrityError as e:
#             print(f"IntegrityError: {e}")
#     conn.commit()

# def update_database_from_csv(folder_path):
#     # Find the database file in the folder
#     db_path = None
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.db'):
#             db_path = os.path.join(folder_path, filename)
#             break

#     if db_path is None:
#         print("No SQLite database file found in the folder.")
#         return

#     # Connect to SQLite database
#     conn = sqlite3.connect(db_path)
    
#     # Create the EmployeesData table if it doesn't exist
#     create_employees_table(conn)
    
#     # Iterate through all files in the folder
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.csv'):
#             file_path = os.path.join(folder_path, filename)
#             # Read the CSV file into a pandas DataFrame
#             data = pd.read_csv(file_path)
            
#             # Infer the table name from the file name (without extension)
#             table_name = os.path.splitext(filename)[0]
            
#             if table_name == 'EmployeesData':
#                 # Drop duplicate rows based on the 'FullName' column
#                 data.drop_duplicates(subset=['FullName'], inplace=True)
                
#                 # Insert data uniquely
#                 insert_data_unique(conn, data, table_name)
#             else:
#                 # Update the database with the CSV data
#                 data.to_sql(table_name, conn, if_exists='append', index=False)
    
#     # Commit changes and close the connection
#     conn.commit()
#     conn.close()

# # Usage
# folder_path = '/Users/macbook/Desktop/ClockInOut'  # Replace with the path to your folder containing both CSV files and the database
# update_database_from_csv(folder_path)




import os
import mysql.connector
import pandas as pd

# Database connection parameters
db_config = {
    'host': '10.183.25.58',  # or 'EGHSVR0044.enighana.intranet'
    'user': 'hafizthesakora',
    'password': 'Mysalmata-1',
    'database': 'enighanaclockinout'
}

def create_connection():
    """Create a database connection and return the connection object."""
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def create_employees_table(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS EmployeesData (
            FullName VARCHAR(255) PRIMARY KEY
        )
    """)
    conn.commit()

def insert_data_unique(conn, data, table_name):
    cursor = conn.cursor()
    for _, row in data.iterrows():
        try:
            cursor.execute(f"INSERT IGNORE INTO {table_name} (FullName) VALUES (%s)", (row['FullName'],))
        except mysql.connector.Error as e:
            print(f"Error: {e}")
    conn.commit()

def update_database_from_csv(folder_path):
    # Connect to MySQL database
    conn = create_connection()
    
    if not conn:
        print("Failed to connect to the database.")
        return
    
    # Create the EmployeesData table if it doesn't exist
    create_employees_table(conn)
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            # Read the CSV file into a pandas DataFrame
            data = pd.read_csv(file_path)
            
            # Infer the table name from the file name (without extension)
            table_name = os.path.splitext(filename)[0]
            
            if table_name == 'EmployeesData':
                # Drop duplicate rows based on the 'FullName' column
                data.drop_duplicates(subset=['FullName'], inplace=True)
                
                # Insert data uniquely
                insert_data_unique(conn, data, table_name)
            else:
                # Update the database with the CSV data
                data.to_sql(table_name, conn, if_exists='append', index=False, method='multi', chunksize=1000)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Usage
folder_path = '/Users/macbook/Desktop/Projects/ClockInOut'  # Replace with the path to your folder containing both CSV files and the database
update_database_from_csv(folder_path)
