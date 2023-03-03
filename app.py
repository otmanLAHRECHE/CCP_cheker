import sys
from PyQt5 import uic, QtWidgets, QtCore ,QtGui, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect, QMessageBox, QFileDialog
from threads import ThreadLoadingVers
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

        self.affichage_ligne = self.findChild(QtWidgets.QCheckBox, "checkBox")
        self.affichage_full_name = self.findChild(QtWidgets.QCheckBox, "checkBox_2")
        self.affichage_rip = self.findChild(QtWidgets.QCheckBox, "checkBox_3")
        self.affichage_valeur = self.findChild(QtWidgets.QCheckBox, "checkBox_4")


        self.filter_ = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.search_with = self.findChild(QtWidgets.QComboBox, "comboBox_2")
        self.search_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")

        self.search = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.reset_search = self.findChild(QtWidgets.QPushButton, "pushButton_4")

        self.champ_compte = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.table_compte = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.import_file_compte = self.findChild(QtWidgets.QToolButton, "toolButton")
        self.reset_compte = self.findChild(QtWidgets.QPushButton, "pushButton")

        self.status_label = self.findChild(QtWidgets.QLabel, "label_18")
        self.status_frame = self.findChild(QtWidgets.QFrame, "frame_26")

        self.file_vers_loaded = False
        self.file_compte_loaded = True

        self.import_file_vers.clicked.connect(self.dialog_load_vers)

        self.scan.clicked.connect(self.scan_event)
        self.reset_vers.clicked.connect(self.reset_vers_event)

        self.accounter = 0

        self.versements_array = []
        self.accounts_array = []


    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def dialog_load_vers(self):
        file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "Text Files (*.txt)")
        if check:
            print(file)
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
            print("okkkkk")
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
            print("ok")


    def reset_vers_event(self):
        self.file_vers_loaded = False
        self.champ_vers.setText("")
        self.total.setText(str(0))
        self.accounter = 0
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
            print(file)
            self.champ_compte.setText(file)
            self.file_compte_loaded = True
            file_compte = open(file)
            self.accounts_array = file_compte.readlines()
            if(len(self.accounts_array)>0):
                self.accounts_array.pop(0)
                self.dialog = Load_account_dialog()
                self.dialog.progress.setValue(0)
                self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog.show()

                self.thr = ThreadLoadingVers(self.accounts_array)
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
            print("okkkkk")
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.close()
            self.file_compte_loaded = True
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
    

        












