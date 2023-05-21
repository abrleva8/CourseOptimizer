import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QApplication, QVBoxLayout, QWidget

# TODO: исправить текст, добавить LaTeX

text = "Объектом оптимизации является химико-технологическая система, состоящая из двух реакторов непрерывного " \
       "действия. В них в результате химического взаимодействия из двух сырьевых компонентов, объемные расходы " \
       "которых А1 и А2 (м^3/ч), образуется целевой компонент в количестве С (кг/ч). " \
       "Для исследования процесса разработана эмпирическая математическая модель, в соответствии с которой количество " \
       "С зависит от объемных расходов компонентов по следующему правилу:\n " \
       "С = α * (A1^2 + β*A2 – µ*V1)^N + α1*(β1*A1 + A2^2 – µ1*V2)^N " \
       "где α, α1, β, β1, µ, µ1 – нормирующие коэффициенты, равные 1; N – количество  реакторов (2 шт.); " \
       "V1 и V2 – рабочие объемы реакторов (11 и 7 м^3 соответственно).\n" \
       "Технологическим регламентом установлены следующие требования к проведению процесса. " \
       "Объемные расходы сырьевых компонентов А1 и А2 могут изменяться в диапазоне от 1 до 10 м^3/ч соответственно;" \
       "кроме того, необходимо, чтобы суммарная производительность реакторов была не больше 8 м^3/час. " \
       "Необходимо найти такие условия проведения процесса (значения А1 и А2)," \
       "при которых обеспечивается максимальный выход целевого компонента в кг за рабочую смену (8 часов). " \
       "Точность решения -0,01 м^3/ч."


class QDialogInfo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Информация")
        self.resize(200, 350)

        layout = QVBoxLayout(self)

        self.program_info = QLabel(text, self)
        self.program_info.setWordWrap(True)
        self.label_img = QLabel(self)
        pixmap = QPixmap('math_problem.png')
        self.label_img.setPixmap(pixmap)
        layout.addWidget(self.program_info, 0)
        layout.addWidget(self.label_img, 1)
        # widget = QWidget()
        # widget.setLayout(layout)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QDialogInfo()
    window.show()

    app.exec()
