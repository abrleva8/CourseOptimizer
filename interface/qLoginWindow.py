from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont

from exceptions.loginException import LoginException
from interface import qDialogInfo
from logic.logic_test import UserWorker


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Регистрация")
        self.setFixedSize(400, 200)
        self._add_components()
        self._center()

    def _add_components(self):
        self.label_login = QLabel("Логин", self)
        self.label_login.move(90, 30)
        self.label_login.setFont(QFont("Sanserif", 15))
        self.input_login = QLineEdit(self)
        self.input_login.move(180, 30)

        self.label_password = QLabel("Пароль", self)
        self.label_password.move(90, 90)
        self.label_password.setFont(QFont("Sanserif", 15))
        self.input_password = QLineEdit(self)
        self.input_password.move(180, 90)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.move(150, 150)
        self.ok_button.clicked.connect(self._ok_clicked)

    def _center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _ok_clicked(self):
        u_worker = UserWorker(self.input_login.text(), self.input_password.text())
        try:
            u_worker.xxx()
            print("aaa")
        except LoginException:
            dlg = qDialogInfo.QDialogInfo(self)
            dlg.setWindowTitle("Ошибка!!!")
            dlg.exec()
