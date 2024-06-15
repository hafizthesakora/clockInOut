from ui_sidebar import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QPushButton, QCompleter, QLabel, QTableWidgetItem, QMessageBox, QFileDialog, QVBoxLayout, QLineEdit, QDialog
from PyQt5.QtCore import Qt, QStandardPaths
from datetime import datetime
from PyQt5 import QtCore
import pandas as pd
import os

import database

class PinEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Confirmation")

        self.valid_pins = ["110098", "779890", "776654"]

        layout = QVBoxLayout()

        self.label = QLabel("Enter the six-digit PIN to confirm your role:")
        layout.addWidget(self.label)

        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pin_input)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def confirm(self):
        entered_pin = self.pin_input.text()
        if entered_pin in self.valid_pins:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "The PIN is unauthorized and cannot export.")


class MySideBar(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Eni Ghana ClockInOut")

        self.employee.setVisible(False)
        self.visitor.setVisible(False)
        self.dashboard.setVisible(False)
        self.pob.setVisible(False)
        self.visitor_dash.setVisible(False)

        self.employee.clicked.connect(self.switch_to_employee)
        self.visitor.clicked.connect(self.switch_to_visitor)
        self.dashboard.clicked.connect(self.switch_to_dashboard)
        self.pob.clicked.connect(self.switch_to_pob)
        self.visitor_dash.clicked.connect(self.switch_to_visitor_dash)

        #Login
        self.username = self.lineEdit_userName
        self.password = self.lineEdit_Password
        self.pushButton_login.clicked.connect(self.login)

        # Employee

        self.name = self.lineEdit_employeeName
        self.dateEdit_employeeDashDateFilter.dateTimeChanged.connect(self.viewEmployeeTransaction)
        self.lineEdit_employeeDashNameFilter.textChanged.connect(self.viewEmployeeTransaction)

        #Visitor
        self.visitorID = self.lineEdit_visitorID
        self.visitorName = self.lineEdit_visitorName
        self.visitorPhone = self.lineEdit_visitorPhone
        self.purpose = self.PurposeofVisit
        self.visitee = self.PersonToVisit
        self.gender = self.Gender
        self.floor = self.Floor
        self.visitorCompany = self.lineEdit_visitorCompany

        #POB
        self.comboBox_personnelType.currentTextChanged.connect(self.filterPOBTable)

        #DateEdits conversion
        self.dateEdit_employeeDashDateFilter.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_employeeDashDateFilter.setDisplayFormat("dd MMM yyyy")

        self.dateEdit_visitorDashDateFilter.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_visitorDashDateFilter.setDisplayFormat("dd MMM yyyy")

        self.dateEdit_clocking.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_clocking.setDisplayFormat("dd MMM yyyy")
        self.dateEdit_clocking.setVisible(False)

        self.dateEdit_visit_clocking.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_visit_clocking.setDisplayFormat("dd MMM yyyy")
        self.dateEdit_visit_clocking.setVisible(False)

        self.dateEdit_visitorDashDateFilter.dateTimeChanged.connect(self.viewVisitorTransaction)
        self.lineEdit_visitorDashNameFilter.textChanged.connect(self.viewVisitorTransaction)

        self.pushButton_employeeDashRefresh.clicked.connect(self.export_confirmation_dialog)
        self.pushButton_visitorDashRefresh.clicked.connect(self.export_visitor_confirmation_dialog)  
        self.pushButton_generateEvacReport.clicked.connect(self.export_pob_confirmation_dialog) 
        

        self.sync()

        #name.textChanged.connect(self.name_completer)
        self.name_completer()
        self.visitor_completer()
        self.visitor_search_completer()
        self.employee_dashboard_completer()


        self.pushButton_clockIN.clicked.connect(self.clockIN)
        self.pushButton_clockOUT.clicked.connect(self.clockOUT)

        self.pushButton_visitorClockIn.clicked.connect(self.visitorClockIN)
        self.pushButton_visitorClockOut.clicked.connect(self.visitorClockOUT)
        self.pushButton_visitorRefresh.clicked.connect(self.visitor_search_btn)

    def switch_to_employee(self):
        self.stackedWidget.setCurrentIndex(0)
    
    def switch_to_visitor(self):
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_dashboard(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_visitor_dash(self):
        self.stackedWidget.setCurrentIndex(5)

    def switch_to_pob(self):
        self.stackedWidget.setCurrentIndex(2)

    #name = self.lineEdit_employeeName

    # employeesName = database.viewData()
    # print(employeesName)
    def sync(self):
        self.name_completer()
        self.visitor_completer()
        self.visitor_search_completer()
        self.employee_dashboard_completer()
        self.visitor_transaction_completer()
        self.viewEmployeeTransaction()
        self.viewVisitorTransaction()
        self.show_POB()

    def name_completer(self):
        employeeName = database.viewData()
        #print(employeeName)
        nameList = []
        for item in employeeName:
            nameList.append(item[0])
        #print(nameList)

        completer = QCompleter(nameList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.name.setCompleter(completer)

     #Login
    def login(self):
        if self.username.text() == "admin" and self.password.text() == "admin@12345":
            self.stackedWidget.setCurrentIndex(0)
            self.employee.setVisible(True)
            self.visitor.setVisible(True)
            self.dashboard.setVisible(True)
            self.pob.setVisible(True)
            self.visitor_dash.setVisible(True)
        else:
            QMessageBox.critical(self, "Error", "Please enter the correct username and password")


            #print(employeeName)
    def clockIN(self):
        name = self.name.text()
        status = 'Clock In'
        #date = datetime.now().strftime("%d %B %Y")
        date = self.dateEdit_clocking.text()
        time = datetime.now().strftime("%H:%M:%S")
        still_in = 'Yes'
        if name == '':
            QMessageBox.critical(self, "Error", "Please enter Employee name")
        else:
            database.insertTransactionData(name, status, time, date, still_in)
            nameList = []
            getPOB = database.view_POBData_Today(date)
            #print('done')
            for item in getPOB:
                #if item[0] not in nameList:
                nameList.append(item[1])
            print('nameList is: ',nameList)
            if name not in nameList:
                database.insert_POBData(name, "Employee", still_in, date)
            else:
                database.update_POBData(still_in, name, date)
            self.name.setText('')
            self.sync()


    def clockOUT(self):
        name = self.name.text()
        status = 'Clock Out'
        #date = datetime.now().strftime("%d %B %Y")
        date = self.dateEdit_clocking.text()
        time = datetime.now().strftime("%H:%M:%S")
        still_in = 'No'
        if name == '':
            QMessageBox.critical(self, "Error", "Please enter Employee name")
        else:
            database.insertTransactionData(name, status, time, date, still_in)
            nameList = []
            getPOB = database.view_POBData_Today(date)
            for item in getPOB:
                #if item[0] not in nameList:
                nameList.append(item[1])

            if name not in nameList:
                print(name , 'is not in List')
                database.insert_POBData(name, "Employee", still_in, date)
            else:
                print(name , 'is in List')
                database.update_POBData(still_in, name, date)
            self.name.setText('')
            self.sync()

    # def export_confirmation_dialog(self):
    #     msgbox = QMessageBox()
    #     msgbox.setText("Click OK to confirm Export")
    #     msgbox.setWindowTitle("Export Confirmation")

    #     # add OK and Cancel btns
    #     msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    #     msgbox.setDefaultButton(QMessageBox.Ok)

    #     # execute msgbox and wait for user's response
    #     response = msgbox.exec_()

    #     if response == QMessageBox.Ok:
    #         self.export_employeeTransaction_toExcel()

   
    def export_confirmation_dialog(self):
        pin_dialog = PinEntryDialog(self)
        response = pin_dialog.exec_()

        if response == QDialog.Accepted:
            self.export_employeeTransaction_toExcel()
        
    def export_employeeTransaction_toExcel(self):
        # try:
        # get column headers as strings
        columnHeaders = [self.tableWidget_employeeDashTable.horizontalHeaderItem(header).text() for header in range(self.tableWidget_employeeDashTable.model().columnCount())]
        # populate dataframe with data
        rows_table = []
        for row in range(self.tableWidget_employeeDashTable.rowCount()):
            # check if row is hidden
            if not self.tableWidget_employeeDashTable.isRowHidden(row):
                row_data = []
                for col in range(self.tableWidget_employeeDashTable.columnCount()):
                    item = self.tableWidget_employeeDashTable.item(row, col)
                    if item is not None:
                        # convert QTableWidget item to string
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                rows_table.append(row_data)
                #print(rows_table)
        # create dataframe with the columns
        df = pd.DataFrame(rows_table, columns = columnHeaders)
        # #set the default directory to user's desktop
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        file_name, _= QFileDialog.getSaveFileName(self, "Save Excel File", os.path.join(desktop_path, "Employee Transaction.xlsx"), "Excel Files (*.xlsx)")

        if file_name:
            # save dataframe to excel
            df.to_excel(file_name, index=False)
            QMessageBox.information(self, "Export", "Excel file exported successfully")
        # except:
        #     QMessageBox.critical(self, "Error", "Can't overwrite an opened Excel file\nConsider changing the name of the exported file\nor closing the opened excel file before exporting") 
        #     return

    

#=============Visitor Entry ================
    def visitor_completer(self):
        employeeName = database.viewData()
        #print(employeeName)
        nameList = []
        for item in employeeName:
            nameList.append(item[0])
        #print(nameList)

        completer = QCompleter(nameList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.visitee.setCompleter(completer)


    def visitor_search_completer(self):
        date = self.dateEdit_visit_clocking.text()
        employeeName = database.viewVisitorData_Today(date)
        #print(employeeName)
        nameList = []
        for item in employeeName:
            nameList.append(item[2])
        #print(nameList)

        completer = QCompleter(nameList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.lineEdit_visitorNameFilter.setCompleter(completer)

    def visitor_search_btn(self):
        visitorName = self.lineEdit_visitorNameFilter.text()
        date = self.dateEdit_visit_clocking.text()
        specific_visitor = database.viewVisitorData_Today_ByName(date,visitorName)

        #print(specific_visitor)
        self.visitorID.setText(specific_visitor[1])
        self.visitorName.setText(specific_visitor[2])
        self.visitorPhone.setText(specific_visitor[3])
        self.purpose.setCurrentText(specific_visitor[5])
        self.visitee.setText(specific_visitor[4])
        self.gender.setCurrentText(specific_visitor[6])
        self.floor.setCurrentText(specific_visitor[7])
        self.visitorCompany.setText(specific_visitor[8])

    def visitorClockIN(self):
        visitorID = self.visitorID.text()
        visitorName = self.visitorName.text()
        visitorPhone = self.visitorPhone.text()
        purpose = self.purpose.currentText() 
        visitee = self.visitee.text()
        gender = self.gender.currentText()
        floor = self.floor.currentText()
        visitorCompany = self.visitorCompany.text()
        status = 'Clock In'
        date = self.dateEdit_visit_clocking.text()
        time = datetime.now().strftime("%H:%M:%S")
        still_in = 'Yes'

        if (visitorName) == '':
            QMessageBox.critical(self, "Error", "Please enter Visitor name")
        else:
            database.insertVisitorData(visitorID, visitorName, visitorPhone, visitee, purpose, gender, floor, visitorCompany, status, time, date, still_in)

            nameList = []
            getPOB = database.view_POBData_Today(date)
            #print('done')
            for item in getPOB:
                #if item[0] not in nameList:
                nameList.append(item[1])
            print('nameList is: ',nameList)
            if visitorName not in nameList:
                database.insert_POBData(visitorName, "Visitor", still_in, date)
            else:
                database.update_POBData(still_in, visitorName, date)

            self.visitorID.setText('')
            self.visitorName.setText('')
            self.visitorPhone.setText('')
            self.purpose.setCurrentText('')
            self.visitee.setText('')
            self.gender.setCurrentText('')
            self.floor.setCurrentText('')
            self.visitorCompany.setText('')
            self.lineEdit_visitorNameFilter.setText('')
            self.sync()


    def visitorClockOUT(self):
        visitorID = self.visitorID.text()
        visitorName = self.visitorName.text()
        visitorPhone = self.visitorPhone.text()
        purpose = self.purpose.currentText()
        visitee = self.visitee.text()
        gender = self.gender.currentText()
        floor = self.floor.currentText()
        visitorCompany = self.visitorCompany.text()
        status = 'Clock Out'
        date = self.dateEdit_visit_clocking.text()
        time = datetime.now().strftime("%H:%M:%S")
        still_in = 'No'
        if visitorName == '':
            QMessageBox.critical(self, "Error", "Please enter Visitor name")
        else:
            database.insertVisitorData(visitorID, visitorName, visitorPhone, visitee, purpose, gender, floor, visitorCompany, status, time, date, still_in)

            nameList = []
            getPOB = database.view_POBData_Today(date)
            #print('done')
            for item in getPOB:
                #if item[0] not in nameList:
                nameList.append(item[1])
            print('nameList is: ',nameList)
            if visitorName not in nameList:
                database.insert_POBData(visitorName, "Visitor", still_in, date)
            else:
                database.update_POBData(still_in, visitorName, date)

            self.visitorID.setText('')
            self.visitorName.setText('')
            self.visitorPhone.setText('')
            self.purpose.setCurrentText('')
            self.visitee.setText('')
            self.gender.setCurrentText('')
            self.floor.setCurrentText('')
            self.visitorCompany.setText('')
            self.lineEdit_visitorNameFilter.setText('')
            self.sync()


    def export_visitor_confirmation_dialog(self):
        pin_dialog = PinEntryDialog(self)
        response = pin_dialog.exec_()

        if response == QDialog.Accepted:
            self.export_visitorTransaction_toExcel()

    def export_visitorTransaction_toExcel(self):
        # try:
        # get column headers as strings
        columnHeaders = [self.tableWidget_visitorDashTable.horizontalHeaderItem(header).text() for header in range(self.tableWidget_visitorDashTable.model().columnCount())]
        # populate dataframe with data
        rows_table = []
        for row in range(self.tableWidget_visitorDashTable.rowCount()):
            # check if row is hidden
            if not self.tableWidget_visitorDashTable.isRowHidden(row):
                row_data = []
                for col in range(self.tableWidget_visitorDashTable.columnCount()):
                    item = self.tableWidget_visitorDashTable.item(row, col)
                    if item is not None:
                        # convert QTableWidget item to string
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                rows_table.append(row_data)
                #print(rows_table)
        # create dataframe with the columns
        df = pd.DataFrame(rows_table, columns = columnHeaders)
        # #set the default directory to user's desktop
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        file_name, _= QFileDialog.getSaveFileName(self, "Save Excel File", os.path.join(desktop_path, "Visitor Transaction.xlsx"), "Excel Files (*.xlsx)")

        if file_name:
            # save dataframe to excel
            df.to_excel(file_name, index=False)
            QMessageBox.information(self, "Export", "Excel file exported successfully")
        # except:
        #     QMessageBox.critical(self, "Error", "Can't overwrite an opened Excel file\nConsider changing the name of the exported file\nor closing the opened excel file before exporting") 
        #     return


#=============Enployee Transaction ================
    def employee_dashboard_completer(self):
        employeeName = database.viewData()
        #print(employeeName)
        nameList = []
        for item in employeeName:
            nameList.append(item[0])
        #print(nameList)

        completer = QCompleter(nameList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.lineEdit_employeeDashNameFilter.setCompleter(completer)

    def viewEmployeeTransaction(self):
        date = self.dateEdit_employeeDashDateFilter.text()
        employeeTransaction = database.viewTransactionData(date)

        #print(employeeTransaction)
        self.tableWidget_employeeDashTable.setRowCount(
            len(employeeTransaction)
        )
        for i, row in enumerate(employeeTransaction):
            for j, value in enumerate(row[1:], start=1):
                item = QTableWidgetItem(str(value))
                self.tableWidget_employeeDashTable.setItem(i, j-1, item)
        self.filterEmployeeTransactionTable()

    def filterEmployeeTransactionTable(self):
        employeedashName = self.lineEdit_employeeDashNameFilter.text()

        for row in range(self.tableWidget_employeeDashTable.rowCount()):
            fullNameEmmployee = self.tableWidget_employeeDashTable.item(row, 0).text()

            name_match = employeedashName.lower() in fullNameEmmployee.lower()
            self.tableWidget_employeeDashTable.setRowHidden(row, not (name_match))









#=============Visitor Transaction ================
    def visitor_transaction_completer(self):
            date = self.dateEdit_visitorDashDateFilter.text()
            employeeName = database.viewVisitorData_Today(date)
            #print(employeeName)
            nameList = []
            for item in employeeName:
                nameList.append(item[2])
            #print(nameList)

            completer = QCompleter(nameList, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            self.lineEdit_visitorDashNameFilter.setCompleter(completer)


    def viewVisitorTransaction(self):
        date = self.dateEdit_visitorDashDateFilter.text()
        #print(date)
        visitorTransaction = database.viewVisitorData_Today(date)
        #print(visitorTransaction)
        self.tableWidget_visitorDashTable.setRowCount(
            len(visitorTransaction)
        )
        for i, row in enumerate(visitorTransaction):
            for j, value in enumerate(row[1:], start=1):
                item = QTableWidgetItem(str(value))
                self.tableWidget_visitorDashTable.setItem(i, j-1, item)
        self.filterVisitorTransactionTable()

    def filterVisitorTransactionTable(self):
            employeedashName = self.lineEdit_visitorDashNameFilter.text()

            for row in range(self.tableWidget_visitorDashTable.rowCount()):
                fullVisitor = self.tableWidget_visitorDashTable.item(row, 1).text()

                name_match = employeedashName.lower() in fullVisitor.lower()
                self.tableWidget_visitorDashTable.setRowHidden(row, not (name_match))        


#============POB Table=======
    def show_POB(self):
        date = self.dateEdit_clocking.text()
        getPOB = database.view_POBData_Today_IN(date)
        print(getPOB)
        self.tableWidget_POBtable.setRowCount(
            len(getPOB)
        )
        for i, row in enumerate(getPOB):
            for j, value in enumerate(row[1:], start=1):
                item = QTableWidgetItem(str(value))
                self.tableWidget_POBtable.setItem(i, j-1, item)
        self.calculate_POB()
        

    def calculate_POB(self):
            count = self.tableWidget_POBtable.rowCount()
            self.lineEdit_NumberOfPeople.setText(str(count))

    def filterPOBTable(self):
            personnelType = self.comboBox_personnelType.currentText()

            for row in range(self.tableWidget_POBtable.rowCount()):
                fullVisitor = self.tableWidget_POBtable.item(row, 1).text()

                name_match = personnelType.lower() in fullVisitor.lower()
                self.tableWidget_POBtable.setRowHidden(row, not (name_match)) 



    def export_pob_confirmation_dialog(self):
        pin_dialog = PinEntryDialog(self)
        response = pin_dialog.exec_()

        if response == QDialog.Accepted:
            self.export_pobTransaction_toExcel()

    def export_pobTransaction_toExcel(self):
        # try:
        # get column headers as strings
        columnHeaders = [self.tableWidget_POBtable.horizontalHeaderItem(header).text() for header in range(self.tableWidget_POBtable.model().columnCount())]
        # populate dataframe with data
        rows_table = []
        for row in range(self.tableWidget_POBtable.rowCount()):
            # check if row is hidden
            if not self.tableWidget_POBtable.isRowHidden(row):
                row_data = []
                for col in range(self.tableWidget_POBtable.columnCount()):
                    item = self.tableWidget_POBtable.item(row, col)
                    if item is not None:
                        # convert QTableWidget item to string
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                rows_table.append(row_data)
                #print(rows_table)
        # create dataframe with the columns
        df = pd.DataFrame(rows_table, columns = columnHeaders)
        # #set the default directory to user's desktop
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        file_name, _= QFileDialog.getSaveFileName(self, "Save Excel File", os.path.join(desktop_path, "Evacuation Report.xlsx"), "Excel Files (*.xlsx)")

        if file_name:
            # save dataframe to excel
            df.to_excel(file_name, index=False)
            QMessageBox.information(self, "Export", "Excel file exported successfully")
        # except:
        #     QMessageBox.critical(self, "Error", "Can't overwrite an opened Excel file\nConsider changing the name of the exported file\nor closing the opened excel file before exporting") 
        #     return