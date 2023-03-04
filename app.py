import sys
from PyQt5 import uic, QtWidgets, QtCore ,QtGui, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect, QMessageBox, QFileDialog, QTableWidgetItem
from threads import ThreadLoadingVers, ThreadLoadingCompte, ThreadScan
from dialogs import Load_versement_dialog, CustomDialog, Load_account_dialog



class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        uic.loadUi("ui/main_ui.ui", self)


        self.tab = self.findChild(QtWidgets.QTableWidget,"tabWidget")

        self.champ_vers = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.table_vers = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.import_file_vers = self.findChild(QtWidgets.QToolButton, "toolButton")
        self.reset_vers = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.scan = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.total = self.findChild(QtWidgets.QLabel, "label_11")

        self.valide = self.findChild(QtWidgets.QLabel, "label_4")
        self.faut_compte = self.findChild(QtWidgets.QLabel, "label_8")
        self.faut_request = self.findChild(QtWidgets.QLabel, "label_9")

        self.filter_ = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.search_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")

        self.champ_compte = self.findChild(QtWidgets.QLineEdit, "lineEdit_3")
        self.table_compte = self.findChild(QtWidgets.QTableWidget, "tableWidget_2")
        self.import_file_compte = self.findChild(QtWidgets.QToolButton, "toolButton_2")
        self.reset_compte = self.findChild(QtWidgets.QPushButton, "pushButton_5")

        self.status_label = self.findChild(QtWidgets.QLabel, "label_18")
        self.status_frame = self.findChild(QtWidgets.QFrame, "frame_26")

        self.search_compte = self.findChild(QtWidgets.QLineEdit, "lineEdit_4")

        self.table_vers.setColumnWidth(0, 180)
        self.table_vers.setColumnWidth(1, 180)
        self.table_vers.setColumnWidth(2, 130)
        self.table_vers.setColumnWidth(3, 180)

        self.table_compte.setColumnWidth(0, 350)
        self.table_compte.setColumnWidth(1, 450)

        
        self.table_compte.setRowCount(0)
        self.table_vers.setRowCount(0)

        self.table_compte.setSortingEnabled(True)
        self.table_vers.setSortingEnabled(True)

        self.file_vers_loaded = False
        self.file_compte_loaded = False

        self.import_file_vers.clicked.connect(self.dialog_load_vers)
        self.import_file_compte.clicked.connect(self.dialog_load_compte)

        self.scan.clicked.connect(self.scan_event)
        self.reset_vers.clicked.connect(self.reset_vers_event)
        self.reset_compte.clicked.connect(self.reset_compte_event)

        self.search_compte.textChanged.connect(self.filter_compte_changed)

        self.search_input.textChanged.connect(self.filter_vers_changed)

        self.accounter = 0
        self.valide_accounter = 0
        self.faut_compte_accounter = 0
        self.faut_request_accounter = 0

        self.versements_array = []
        self.accounts_array = []
        self.result_array = []


    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def dialog_load_vers(self):
        file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "Text Files (*.txt)")
        if check:
            self.reset_vers_event()
            self.champ_vers.setText(file)
            self.file_vers_loaded = True
            file_vers = open(file)
            self.versements_array = file_vers.readlines()
            self.accounter = 0
            self.total.setText(str(0))
            if(len(self.versements_array)>0):
                self.versements_array.pop(0)
                self.dialog = Load_versement_dialog()
                self.dialog.progress.setValue(0)
                self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog.show()

                self.thr = ThreadLoadingVers(self.versements_array)
                self.thr._signal.connect(self.signal_progress)
                self.thr._signal_result.connect(self.signal_progress)
                self.thr._signal_result_data.connect(self.signal_progress)
                self.thr._signal_show.connect(self.signal_aff)
                self.thr.start()
            else:
                self.alert_("le fichier est vide")
            

    def signal_progress(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:
            self.versements_array = progress
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.close()
            self.file_vers_loaded = True
            if(self.file_compte_loaded == True):
                self.status_label.setText("status: ready")
                stylesheet = \
                "color:white;\n" \
                + "background:qlineargradient(spread:pad, x1:1, y1:0.545, x2:0, y2:0.585, stop:0 rgba(2, 36, 0, 73), stop:24 rgba(36, 157, 17, 100), stop:100 rgba(0, 255, 119, 100));" 
                self.status_frame.setStyleSheet(stylesheet)
            else:
                stylesheet = \
                "color:white;\n" \
                + "background:qlineargradient(spread:pad, x1:1, y1:0.545, x2:0, y2:0.585, stop:0 rgba(184, 21, 21, 57), stop:0.487 rgba(182, 27, 13, 186), stop:1 rgba(184, 21, 21, 57));" 
                self.status_frame.setStyleSheet(stylesheet)
                self.status_label.setText("status: not ready (import account file)")

    
    def signal_aff(self, progress):
        if type(progress) == list:
            self.dialog.full_name.setText(progress[0])
            self.dialog.rip.setText(progress[1])
            self.dialog.valeur.setText(str(progress[2]))
            self.accounter = self.accounter + 1
            self.total.setText(str(self.accounter))


    def scan_event(self):
        if(self.file_vers_loaded == False or self.file_compte_loaded == False):
            self.alert_("importer le fichier .txt")
        else:
            
            self.dialog = Load_versement_dialog()
            self.dialog.progress.setValue(0)
            self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.dialog.show()

            self.thr = ThreadScan(self.versements_array, self.accounts_array)
            self.thr._signal.connect(self.signal_progress_scan)
            self.thr._signal_result.connect(self.signal_progress_scan)
            self.thr._signal_result_data.connect(self.signal_progress_scan)
            self.thr._signal_show.connect(self.signal_aff_scan)
            self.thr.start()
            
    
    def signal_progress_scan(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:
            self.result_array = progress
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.close()

    def signal_aff_scan(self, progress):
        if type(progress) == list:
            self.dialog.full_name.setText(progress[0])
            self.dialog.rip.setText(progress[1])
            self.dialog.valeur.setText(str(progress[2]))

            row = self.table_vers.rowCount()
            if(progress[3]=="valide"):
                self.table_vers.insertRow(row)   
                self.table_vers.setItem(row, 0, QTableWidgetItem(progress[0]))
                self.table_vers.setItem(row, 1, QTableWidgetItem(progress[1]))
                self.table_vers.setItem(row, 2, QTableWidgetItem(str(progress[2])))
                self.table_vers.setItem(row, 3, QTableWidgetItem(str(progress[3])))
                self.table_vers.item(row, 0).setBackground(QColor(220,255,220))
                self.table_vers.item(row, 1).setBackground(QColor(220,255,220))
                self.table_vers.item(row, 2).setBackground(QColor(220,255,220))
                self.table_vers.item(row, 3).setBackground(QColor(220,255,220))
                self.valide_accounter = self.valide_accounter + 1
                self.valide.setText(str(self.valide_accounter))
            elif(progress[3]=="faut compte!!"):
                self.table_vers.insertRow(row)   
                self.table_vers.setItem(row, 0, QTableWidgetItem(progress[0]))
                self.table_vers.setItem(row, 1, QTableWidgetItem(progress[1]))
                self.table_vers.setItem(row, 2, QTableWidgetItem(str(progress[2])))
                self.table_vers.setItem(row, 3, QTableWidgetItem(str(progress[3])))
                self.table_vers.item(row, 0).setBackground(QColor(247, 96, 96))
                self.table_vers.item(row, 1).setBackground(QColor(247, 96, 96))
                self.table_vers.item(row, 2).setBackground(QColor(247, 96, 96))
                self.table_vers.item(row, 3).setBackground(QColor(247, 96, 96))
                self.faut_compte_accounter = self.faut_compte_accounter + 1
                self.faut_compte.setText(str(self.faut_compte_accounter))
            elif(progress[3]=="n'existe pas sur DB"):
                self.table_vers.insertRow(row)   
                self.table_vers.setItem(row, 0, QTableWidgetItem(progress[0]))
                self.table_vers.setItem(row, 1, QTableWidgetItem(progress[1]))
                self.table_vers.setItem(row, 2, QTableWidgetItem(str(progress[2])))
                self.table_vers.setItem(row, 3, QTableWidgetItem(str(progress[3])))
                self.table_vers.item(row, 0).setBackground(QColor(247, 237, 96))
                self.table_vers.item(row, 1).setBackground(QColor(247, 237, 96))
                self.table_vers.item(row, 2).setBackground(QColor(247, 237, 96))
                self.table_vers.item(row, 3).setBackground(QColor(247, 237, 96))
                self.faut_request_accounter = self.faut_request_accounter + 1
                self.faut_request.setText(str(self.faut_request_accounter))


    def reset_vers_event(self):
        self.file_vers_loaded = False
        self.versements_array = []
        self.result_array = []
        self.table_vers.setRowCount(0)
        self.champ_vers.setText("")
        self.total.setText(str(0))
        self.valide.setText(str(0))
        self.faut_request.setText(str(0))
        self.faut_compte.setText(str(0))
        self.accounter = 0
        self.valide_accounter = 0
        self.faut_compte_accounter = 0
        self.faut_request_accounter = 0
        if(self.file_compte_loaded == True):
            stylesheet = \
            "color:white;\n" \
            + "background:qlineargradient(spread:pad, x1:1, y1:0.545, x2:0, y2:0.585, stop:0 rgba(184, 21, 21, 57), stop:0.487 rgba(182, 27, 13, 186), stop:1 rgba(184, 21, 21, 57));" 
            self.status_frame.setStyleSheet(stylesheet)
            self.status_label.setText("status: not ready (import versement file)")
        else:
            stylesheet = \
            "color:white;\n" \
            + "background:qlineargradient(spread:pad, x1:1, y1:0.545, x2:0, y2:0.585, stop:0 rgba(184, 21, 21, 57), stop:0.487 rgba(182, 27, 13, 186), stop:1 rgba(184, 21, 21, 57));" 
            self.status_frame.setStyleSheet(stylesheet)
            self.status_label.setText("status: not ready (import account file)")

    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "Es-tu sûr de quiter?"
        dialog = CustomDialog(message)
        if dialog.exec():
            self.close()
        else:
            a0.ignore()

    
    def dialog_load_compte(self):
        file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "Text Files (*.txt)")
        if check:
            self.reset_compte_event()
            self.champ_compte.setText(file)
            self.file_compte_loaded = True
            file_compte = open(file)
            self.accounts_array = file_compte.readlines()
            self.dup = 0
            if(len(self.accounts_array)>0):
                self.accounts_array.pop(0)
                self.dialog = Load_account_dialog()
                self.dialog.progress.setValue(0)
                self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog.show()

                self.thr = ThreadLoadingCompte(self.accounts_array)
                self.thr._signal.connect(self.signal_progress_account)
                self.thr._signal_result.connect(self.signal_progress_account)
                self.thr._signal_result_data.connect(self.signal_progress_account)
                self.thr._signal_show.connect(self.signal_aff_account)
                self.thr.start()
            else:
                self.alert_("le fichier est vide")
    

    def signal_progress_account(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:
            self.accounts_array = progress
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.close()
            self.file_compte_loaded = True
            if(self.dup > 0):
                self.alert_("supprimer les duplications")
            if(self.file_vers_loaded == True):
                self.status_label.setText("status: ready")
                stylesheet = \
                "color:white;\n" \
                + "background:qlineargradient(spread:pad, x1:1, y1:0.545, x2:0, y2:0.585, stop:0 rgba(2, 36, 0, 73), stop:24 rgba(36, 157, 17, 100), stop:100 rgba(0, 255, 119, 100));" 
                self.status_frame.setStyleSheet(stylesheet)
            else:
                stylesheet = \
                "color:white;\n" \
                + "background:qlineargradient(spread:pad, x1:1, y1:0.545, x2:0, y2:0.585, stop:0 rgba(184, 21, 21, 57), stop:0.487 rgba(182, 27, 13, 186), stop:1 rgba(184, 21, 21, 57));" 
                self.status_frame.setStyleSheet(stylesheet)
                self.status_label.setText("status: not ready (import versement file)")
            

    def signal_aff_account(self, progress):
        if type(progress) == list:
            self.dialog.full_name.setText(progress[0])
            self.dialog.rip.setText(progress[1])

            row = self.table_compte.rowCount()
            if(progress[2]=="dup"):
                self.table_compte.insertRow(row)   
                self.table_compte.setItem(row, 0, QTableWidgetItem(progress[0]))
                self.table_compte.setItem(row, 1, QTableWidgetItem(progress[1]))
                self.table_compte.item(row, 0).setBackground(QColor(220, 242, 24))
                self.table_compte.item(row, 1).setBackground(QColor(220, 242, 24))
                self.dup = self.dup + 1
            else:
                self.table_compte.insertRow(row)   
                self.table_compte.setItem(row, 0, QTableWidgetItem(progress[0]))
                self.table_compte.setItem(row, 1, QTableWidgetItem(progress[1]))
                self.table_compte.item(row, 0).setBackground(QColor(220,255,220))
                self.table_compte.item(row, 1).setBackground(QColor(220,255,220))
            
    
    def reset_compte_event(self):
        self.file_compte_loaded = False
        self.accounts_array = []
        self.table_compte.setRowCount(0)
        self.champ_compte.setText("")
        self.dup = 0   
        stylesheet = \
        "color:white;\n" \
        + "background:qlineargradient(spread:pad, x1:1, y1:0.545, x2:0, y2:0.585, stop:0 rgba(184, 21, 21, 57), stop:0.487 rgba(182, 27, 13, 186), stop:1 rgba(184, 21, 21, 57));" 
        self.status_frame.setStyleSheet(stylesheet)
        self.status_label.setText("status: not ready (import account file)")
    

    def filter_account_apr(self, filter_text):
        for i in range(self.table_compte.rowCount()):
            for j in range(self.table_compte.columnCount()):
                item = self.table_compte.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.table_compte.setRowHidden(i, match)
                if not match:
                    break


    def filter_compte_changed(self, text):
        self.filter_account_apr(text)


    def filter_vers_apr(self, filter_text):
        for i in range(self.table_vers.rowCount()):
            for j in range(self.table_vers.columnCount()-2):
                item = self.table_vers.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.table_vers.setRowHidden(i, match)
                if not match:
                    break


    def filter_vers_changed(self, text):
        self.filter_vers_apr(text)













