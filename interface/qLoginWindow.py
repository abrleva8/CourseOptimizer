from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont

from exceptions.loginException import LoginException
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
        self.input_login.setFixedWidth(150)
        self.input_login.textChanged.connect(self._input_text_changed)
        self.input_login.setPlaceholderText('Введите непустой логин')

        self.label_password = QLabel("Пароль", self)
        self.label_password.move(90, 90)
        self.label_password.setFont(QFont("Sanserif", 15))

        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.move(180, 90)
        self.input_password.setFixedWidth(150)
        self.input_password.textChanged.connect(self._input_text_changed)
        self.input_password.setPlaceholderText('Введите пароль')

        self.ok_button = QPushButton("OK", self)
        self.ok_button.move(150, 150)
        self.ok_button.clicked.connect(self._ok_clicked)
        self.ok_button.setEnabled(False)

    def _center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _input_text_changed(self, string):
        if string:
            self.ok_button.setEnabled(True)
        else:
            self.ok_button.setEnabled(False)

    def _ok_clicked(self):
        u_worker = UserWorker(self.input_login.text(), self.input_password.text())
        try:
            u_worker.xxx()
            print("aaa")
        except LoginException as le:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Ошибка!")
            dlg.setIcon(QMessageBox.Icon.Critical)
            dlg.setText(str(le))
            dlg.exec()
