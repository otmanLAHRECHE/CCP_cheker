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
        self.scan_vers = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        









