import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect



class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        uic.loadUi("ui/main_ui.ui", self)

        