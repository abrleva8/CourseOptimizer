from PyQt6.QtWidgets import QDialog


class QDialogInfo(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Информация")

