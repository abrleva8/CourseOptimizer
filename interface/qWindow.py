from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QToolBar, QWidget, QDialog
from interface import qDialogInfo


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Курсовая работа, 1 вариант")
        self.resize(1000, 700)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Информация", self)
        button_action.setToolTip("Формулировка задачи курсового проекта")
        button_action.triggered.connect(self.xxx)
        # button_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action)

    def xxx(self, s):
        dlg = qDialogInfo.QDialogInfo(self)
        dlg.setWindowTitle("Формулировка задачи")
        dlg.exec()
