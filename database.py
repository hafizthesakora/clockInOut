# import sqlite3

# import os

# # # Get the path to the user's AppData\Local  directory
# # appdata_dir = os.path.expanduser(os.path.join("~", "AppData", 'Local'))

# # #Create a directory for application if it doesn't exist
# # app_dir = os.path.join(appdata_dir, "EniGhanaClockInOut")
# # os.makedirs(app_dir, exist_ok=True)

# # #Define the name of the Db file
# # db_filename = "EniGhanaClockInOut.db"

# # #Construct the full path to the database file
# # db_path = os.path.join(app_dir, db_filename)

# db_path = "EniGhanaClockInOut.db"

# def EmployeesData():
#     # if not os.path.exists(db_path):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS EmployeesData (FullName text PRIMARY KEY)")
#     con.commit()
#     con.close()

# def viewData():
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("SELECT * FROM EmployeesData")
#     rows = cur.fetchall()
#     con.close()
#     return rows

# # ============== Employees transaction table ======
# def EmployeesTransaction():
#     # if not os.path.exists(db_path):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS EmployeesTransactionTable (ID integer PRIMARY KEY, FullName text, CLOCKINSTATUS text, myTime text, myDate text, still_in text )")
#     con.commit()
#     con.close()

# def viewAllTransactionData():
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("SELECT * FROM EmployeesTransactionTable")
#     rows = cur.fetchall()
#     con.close()
#     return rows

# def viewTransactionData(myDate):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("SELECT * FROM EmployeesTransactionTable WHERE myDate=?", (myDate,))
#     rows = cur.fetchall()
#     con.close()
#     return rows

# def insertTransactionData(FullName, CLOCKINSTATUS, myTime, myDate, still_in):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("INSERT INTO EmployeesTransactionTable VALUES (NULL, ?,?,?,?,?)", (FullName, CLOCKINSTATUS, myTime, myDate, still_in))
#     #rows = cur.fetchall()
#     con.commit()
#     con.close()


# # ============== Visitor Entry table ======
# def VisitorData():
#     # if not os.path.exists(db_path):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS VisitorDataTable (ID integer PRIMARY KEY, VisitorID text, VisitorName text, VisitorPhoneNumber text, PersonToVisit text, PurposeOfVisit text, Gender text, Floor text, VisitorCompany text, CLOCKINSTATUS text, myTime text, myDate text, still_in )")
#     con.commit()
#     con.close()

# def viewVisitorData():
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("SELECT * FROM VisitorDataTable")
#     rows = cur.fetchall()
#     con.close()
#     return rows

# def viewVisitorData_Today(myDate):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("SELECT * FROM VisitorDataTable WHERE myDate=?", (myDate,))
#     rows = cur.fetchall()
#     con.close()
#     return rows

# def viewVisitorData_Today_ByName(myDate, VisitorName):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("SELECT * FROM VisitorDataTable WHERE myDate=? AND VisitorName=?", (myDate, VisitorName,))
#     rows = cur.fetchone()
#     con.close()
#     return rows

# def insertVisitorData(VisitorID, VisitorName, VisitorPhoneNumber, PersonToVisit, PurposeOfVisit, Gender, Floor, VisitorCompany, CLOCKINSTATUS, myTime, myDate, still_in ):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("INSERT INTO VisitorDataTable VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?)", (VisitorID, VisitorName, VisitorPhoneNumber, PersonToVisit, PurposeOfVisit, Gender, Floor, VisitorCompany, CLOCKINSTATUS, myTime, myDate, still_in))
#     #rows = cur.fetchall()
#     con.commit()
#     con.close()





# #=============POB Table=========================
# def POBData():
#     # if not os.path.exists(db_path):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS POBTable (ID integer PRIMARY KEY, Name text, PersonnelType text, Still_in text, myDate text)")
#     con.commit()
#     con.close()

# def insert_POBData(Name, PersonnelType, Still_in, myDate):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("INSERT INTO POBTable VALUES (NULL, ?,?,?,?)", (Name, PersonnelType, Still_in, myDate))
#     con.commit()
#     con.close()

# def view_POBData_Today(myDate):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("SELECT * FROM POBTable WHERE myDate=?", (myDate,))
#     rows = cur.fetchall()
#     con.close()
#     return rows

# def view_POBData_Today_IN(myDate):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("SELECT * FROM POBTable WHERE myDate=? AND Still_in='Yes'", (myDate,))
#     rows = cur.fetchall()
#     con.close()
#     return rows

# def update_POBData(Still_in, Name, myDate):
#     con = sqlite3.connect(db_path)
#     cur = con.cursor()
#     cur.execute("UPDATE POBTable SET Still_in=? WHERE Name=? AND myDate=?",(Still_in, Name, myDate))
#     con.commit()
#     con.close()


# EmployeesData()
# EmployeesTransaction()
# VisitorData()
# POBData()

# data = viewTransactionData()
# print(data)

#insertTransactionData('James', 'in', 45, 4, 'yes')






import mysql.connector
from mysql.connector import Error

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
        con = mysql.connector.connect(**db_config)
        if con.is_connected():
            return con
    except Error as e:
        print(f"Error: {e}")
        return None

def EmployeesData():
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS EmployeesData (FullName VARCHAR(255) PRIMARY KEY)")
        con.commit()
        con.close()

def viewData():
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM EmployeesData")
        rows = cur.fetchall()
        con.close()
        return rows

def EmployeesTransaction():
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS EmployeesTransactionTable (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                FullName VARCHAR(255),
                CLOCKINSTATUS VARCHAR(255),
                myTime VARCHAR(255),
                myDate VARCHAR(255),
                still_in VARCHAR(255)
            )
        """)
        con.commit()
        con.close()

def viewAllTransactionData():
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM EmployeesTransactionTable")
        rows = cur.fetchall()
        con.close()
        return rows

def viewTransactionData(myDate):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM EmployeesTransactionTable WHERE myDate=%s", (myDate,))
        rows = cur.fetchall()
        con.close()
        return rows

def insertTransactionData(FullName, CLOCKINSTATUS, myTime, myDate, still_in):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("INSERT INTO EmployeesTransactionTable (FullName, CLOCKINSTATUS, myTime, myDate, still_in) VALUES (%s, %s, %s, %s, %s)", (FullName, CLOCKINSTATUS, myTime, myDate, still_in))
        con.commit()
        con.close()

def VisitorData():
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS VisitorDataTable (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                VisitorID VARCHAR(255),
                VisitorName VARCHAR(255),
                VisitorPhoneNumber VARCHAR(255),
                PersonToVisit VARCHAR(255),
                PurposeOfVisit VARCHAR(255),
                Gender VARCHAR(255),
                Floor VARCHAR(255),
                VisitorCompany VARCHAR(255),
                CLOCKINSTATUS VARCHAR(255),
                myTime VARCHAR(255),
                myDate VARCHAR(255),
                still_in VARCHAR(255)
            )
        """)
        con.commit()
        con.close()

def viewVisitorData():
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM VisitorDataTable")
        rows = cur.fetchall()
        con.close()
        return rows

def viewVisitorData_Today(myDate):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM VisitorDataTable WHERE myDate=%s", (myDate,))
        rows = cur.fetchall()
        con.close()
        return rows

def viewVisitorData_Today_ByName(myDate, VisitorName):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM VisitorDataTable WHERE myDate=%s AND VisitorName=%s", (myDate, VisitorName))
        rows = cur.fetchone()
        con.close()
        return rows

def insertVisitorData(VisitorID, VisitorName, VisitorPhoneNumber, PersonToVisit, PurposeOfVisit, Gender, Floor, VisitorCompany, CLOCKINSTATUS, myTime, myDate, still_in):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("INSERT INTO VisitorDataTable (VisitorID, VisitorName, VisitorPhoneNumber, PersonToVisit, PurposeOfVisit, Gender, Floor, VisitorCompany, CLOCKINSTATUS, myTime, myDate, still_in) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (VisitorID, VisitorName, VisitorPhoneNumber, PersonToVisit, PurposeOfVisit, Gender, Floor, VisitorCompany, CLOCKINSTATUS, myTime, myDate, still_in))
        con.commit()
        con.close()

def POBData():
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS POBTable (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255),
                PersonnelType VARCHAR(255),
                Still_in VARCHAR(255),
                myDate VARCHAR(255)
            )
        """)
        con.commit()
        con.close()

def insert_POBData(Name, PersonnelType, Still_in, myDate):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("INSERT INTO POBTable (Name, PersonnelType, Still_in, myDate) VALUES (%s, %s, %s, %s)", (Name, PersonnelType, Still_in, myDate))
        con.commit()
        con.close()

def view_POBData_Today(myDate):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM POBTable WHERE myDate=%s", (myDate,))
        rows = cur.fetchall()
        con.close()
        return rows

def view_POBData_Today_IN(myDate):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("SELECT * FROM POBTable WHERE myDate=%s AND Still_in='Yes'", (myDate,))
        rows = cur.fetchall()
        con.close()
        return rows

def update_POBData(Still_in, Name, myDate):
    con = create_connection()
    if con:
        cur = con.cursor()
        cur.execute("UPDATE POBTable SET Still_in=%s WHERE Name=%s AND myDate=%s", (Still_in, Name, myDate))
        con.commit()
        con.close()

# Initialize the database tables
EmployeesData()
EmployeesTransaction()
VisitorData()
POBData()

# Example usage
# data = viewTransactionData('2024-06-12')
# print(data)

# insertTransactionData('James', 'in', '10:45', '2024-06-12', 'yes')
