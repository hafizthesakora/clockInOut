import sqlite3

import os

# # Get the path to the user's AppData\Local  directory
# appdata_dir = os.path.expanduser(os.path.join("~", "AppData", 'Local'))

# #Create a directory for application if it doesn't exist
# app_dir = os.path.join(appdata_dir, "EniGhanaClockInOut")
# os.makedirs(app_dir, exist_ok=True)

# #Define the name of the Db file
# db_filename = "EniGhanaClockInOut.db"

# #Construct the full path to the database file
# db_path = os.path.join(app_dir, db_filename)

db_path = "EniGhanaClockInOut.db"

def EmployeesData():
    # if not os.path.exists(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS EmployeesData (FullName text PRIMARY KEY)")
    con.commit()
    con.close()

def viewData():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM EmployeesData")
    rows = cur.fetchall()
    con.close()
    return rows

# ============== Employees transaction table ======
def EmployeesTransaction():
    # if not os.path.exists(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS EmployeesTransactionTable (ID integer PRIMARY KEY, FullName text, CLOCKINSTATUS text, myTime text, myDate text, still_in text )")
    con.commit()
    con.close()

def viewAllTransactionData():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM EmployeesTransactionTable")
    rows = cur.fetchall()
    con.close()
    return rows

def viewTransactionData(myDate):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM EmployeesTransactionTable WHERE myDate=?", (myDate,))
    rows = cur.fetchall()
    con.close()
    return rows

def insertTransactionData(FullName, CLOCKINSTATUS, myTime, myDate, still_in):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO EmployeesTransactionTable VALUES (NULL, ?,?,?,?,?)", (FullName, CLOCKINSTATUS, myTime, myDate, still_in))
    #rows = cur.fetchall()
    con.commit()
    con.close()


# ============== Visitor Entry table ======
def VisitorData():
    # if not os.path.exists(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS VisitorDataTable (ID integer PRIMARY KEY, VisitorID text, VisitorName text, VisitorPhoneNumber text, PersonToVisit text, PurposeOfVisit text, Gender text, Floor text, VisitorCompany text, CLOCKINSTATUS text, myTime text, myDate text, still_in )")
    con.commit()
    con.close()

def viewVisitorData():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM VisitorDataTable")
    rows = cur.fetchall()
    con.close()
    return rows

def viewVisitorData_Today(myDate):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM VisitorDataTable WHERE myDate=?", (myDate,))
    rows = cur.fetchall()
    con.close()
    return rows

def viewVisitorData_Today_ByName(myDate, VisitorName):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM VisitorDataTable WHERE myDate=? AND VisitorName=?", (myDate, VisitorName,))
    rows = cur.fetchone()
    con.close()
    return rows

def insertVisitorData(VisitorID, VisitorName, VisitorPhoneNumber, PersonToVisit, PurposeOfVisit, Gender, Floor, VisitorCompany, CLOCKINSTATUS, myTime, myDate, still_in ):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO VisitorDataTable VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?)", (VisitorID, VisitorName, VisitorPhoneNumber, PersonToVisit, PurposeOfVisit, Gender, Floor, VisitorCompany, CLOCKINSTATUS, myTime, myDate, still_in))
    #rows = cur.fetchall()
    con.commit()
    con.close()





#=============POB Table=========================
def POBData():
    # if not os.path.exists(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS POBTable (ID integer PRIMARY KEY, Name text, PersonnelType text, Still_in text, myDate text)")
    con.commit()
    con.close()

def insert_POBData(Name, PersonnelType, Still_in, myDate):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO POBTable VALUES (NULL, ?,?,?,?)", (Name, PersonnelType, Still_in, myDate))
    con.commit()
    con.close()

def view_POBData_Today(myDate):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM POBTable WHERE myDate=?", (myDate,))
    rows = cur.fetchall()
    con.close()
    return rows

def view_POBData_Today_IN(myDate):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM POBTable WHERE myDate=? AND Still_in='Yes'", (myDate,))
    rows = cur.fetchall()
    con.close()
    return rows

def update_POBData(Still_in, Name, myDate):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("UPDATE POBTable SET Still_in=? WHERE Name=? AND myDate=?",(Still_in, Name, myDate))
    con.commit()
    con.close()


EmployeesData()
EmployeesTransaction()
VisitorData()
POBData()

# data = viewTransactionData()
# print(data)

#insertTransactionData('James', 'in', 45, 4, 'yes')