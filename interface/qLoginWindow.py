import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QApplication, QWidget

from exceptions import LoginException
from interface import qWindow
from logic import UserWorker


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")

        layout = self._get_layout()
        self.setLayout(layout)
        self.setFixedSize(300, 150)
        self._center()

    def _get_layout(self):
        layout = QGridLayout()
        title = QLabel("Окно регистрации")
        layout.addWidget(title, 0, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        label_login = QLabel("Логин")
        layout.addWidget(label_login, 1, 0)

        self.input_login = QLineEdit("")
        self.input_login.setPlaceholderText('Введите непустой логин')
        self.input_login.textChanged.connect(self._input_text_changed)

        layout.addWidget(self.input_login, 1, 1, 1, 3)
        label_password = QLabel("Пароль")
        layout.addWidget(label_password, 2, 0)

        self.input_password = QLineEdit("")
        self.input_password.setPlaceholderText('Введите пароль')
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.input_password, 2, 1, 1, 3)
        self.ok_button = QPushButton("OK")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self._ok_clicked)
        layout.addWidget(self.ok_button, 3, 1, 1, 2)
        return layout

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
            login = u_worker.get_login()
        except LoginException as le:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Ошибка!")
            dlg.setIcon(QMessageBox.Icon.Critical)
            dlg.setText(str(le))
            dlg.exec()
            return

        match login:
            case 'adminl':
                self.main_window = qWindow.MainWindow()
                self.main_window.show()
                self.close()
            case 'loginl':
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()

    app.exec()
