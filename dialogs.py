
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QDialogButtonBox, QVBoxLayout, QLabel



class Load_versement_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Load_versement_dialog, self).__init__()
        uic.loadUi("./ui/dialog_load_vers.ui", self)
        self.setWindowTitle("importer les versement")

        self.full_name = self.findChild(QtWidgets.QLabel, "label_4")
        self.rip = self.findChild(QtWidgets.QLabel, "label_5")
        self.valeur = self.findChild(QtWidgets.QLabel, "label_6")

        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")