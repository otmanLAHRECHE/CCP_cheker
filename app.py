import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect



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
        self.affichage_ccp = self.findChild(QtWidgets.QCheckBox, "checkBox_5")
        self.affichage_rip = self.findChild(QtWidgets.QCheckBox, "checkBox_3")
        self.affichage_valeur = self.findChild(QtWidgets.QCheckBox, "checkBox_4")

        










