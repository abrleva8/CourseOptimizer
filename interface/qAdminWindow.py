import sys

from PyQt6.QtWidgets import QWidget, QApplication, QComboBox, QPushButton, QGridLayout, QLineEdit, QMessageBox
from PyQt6 import QtGui

import logic
from exceptions import AdminException


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно администратора")
        self.admin_worker = logic.AdminWorker()
        self.setFixedSize(300, 150)

        layout = self._get_layout()
        self.setLayout(layout)

        self._init_methods_combo_box()

        self._center()

    def _get_layout(self):
        layout = QGridLayout()

        self.methods_combo_box = QComboBox(self)
        self.methods_combo_box.currentTextChanged.connect(self._methods_combo_box_changed)
        layout.addWidget(self.methods_combo_box, 0, 0)

        self.delete_button = QPushButton(self)
        self.delete_button.setText("Удалить метод")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self._delete_button_clicked)
        layout.addWidget(self.delete_button, 0, 1)

        self.input_add_new_method = QLineEdit("")
        self.input_add_new_method.setPlaceholderText('Введите новый метод')
        self.input_add_new_method.textChanged.connect(self._input_add_new_method_changed)
        layout.addWidget(self.input_add_new_method, 1, 0)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить метод")
        self.add_button.setEnabled(False)
        layout.addWidget(self.add_button, 1, 1)
        self.add_button.clicked.connect(self._add_button_clicked)

        return layout

    def _center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _init_methods_combo_box(self):
        list_of_methods = self.admin_worker.get_methods()
        name_of_methods = list(map(lambda x: x[0], list_of_methods))
        self.methods_combo_box.clear()
        self.methods_combo_box.addItems(name_of_methods)

    def _add_button_clicked(self):
        method_name = self.input_add_new_method.text()
        # self.methods_combo_box.itemData()
        self.admin_worker.insert_method(method_name)
        self._init_methods_combo_box()

    # TODO: сообщение о удачном или неудачном удалении
    def _delete_button_clicked(self):
        content = self.methods_combo_box.currentText()
        try:
            self.admin_worker.delete_method(content)
        except AdminException as e:
            self._show_message_nelder_mead(e)
        self._init_methods_combo_box()

    def _methods_combo_box_changed(self):
        content = self.methods_combo_box.currentText()
        if content:
            self.delete_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)

    def _input_add_new_method_changed(self):
        content = self.input_add_new_method.text()
        if content:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def _show_message_nelder_mead(self, e):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Ошибка!")
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.setText(str(e))
        dlg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()

    app.exec()
