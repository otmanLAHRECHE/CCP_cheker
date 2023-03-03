
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


class CustomDialog(QtWidgets.QDialog):
    def __init__(self, msg, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Alert")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)