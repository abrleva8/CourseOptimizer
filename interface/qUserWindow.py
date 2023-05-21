import sys

import matplotlib
from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QGridLayout, QLabel, QHBoxLayout, QLineEdit
from PyQt6.QtWidgets import QToolBar
from matplotlib import cm

from interface import qDialogInfo, qLoginWindow
from logic import Optimizer
from plotting.mpl_canvas import MplCanvas

matplotlib.use('QtAgg')


class UserWindow(QMainWindow):
    def __init__(self):
        super(UserWindow, self).__init__()

        # TODO: сделать рефакторинг: вынести графики в отдельный модуль
        self.minimum_point_3d = None

        self.setWindowTitle("Курсовая работа, 1 вариант")
        self.showMaximized()
        self._add_components()

        # TODO: сделать рефакторинг
        self.i = 0

        self.optimizer = Optimizer()
        self.show()

    def _add_components(self):

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Информация", self)
        button_action.setToolTip("Формулировка задачи курсового проекта")
        button_action.triggered.connect(self._open_dialog_info)
        toolbar.addAction(button_action)

        button_change_user = QAction("Сменить пользователя", self)
        button_change_user.setToolTip("Сменить пользователя")
        button_change_user.triggered.connect(self._change_user)
        toolbar.addAction(button_change_user)

        self.label_count_iteration = QLabel("Число итерации")

        self.input_count_iteration = QLineEdit("10")
        self.input_count_iteration.setPlaceholderText('Введите число итерации')
        self.input_count_iteration.setInputMask("d0")

        self.ok_button = QPushButton("Нарисовать графики", self)
        self.ok_button.clicked.connect(self._start_clicked)
        self.ok_button.setEnabled(True)

        self.founded_optimum_point = QLabel("Точка максимума: ", self)
        self.founded_optimum_value = QLabel("Найденный максимум: ", self)

        self.canvas = MplCanvas(width=4, height=4, dpi=100)

        layout_t = QHBoxLayout(self)

        layout_left = QGridLayout()
        layout_right = QGridLayout()
        layout_left.addWidget(self.label_count_iteration, 0, 0)
        layout_left.addWidget(self.input_count_iteration, 0, 1)
        layout_left.addWidget(self.ok_button, 1, 0)
        layout_left.addWidget(self.founded_optimum_point, 2, 0)
        layout_left.addWidget(self.founded_optimum_value, 3, 0)
        layout_right.addWidget(self.canvas)

        layout_t.addLayout(layout_left, 0)
        layout_t.addLayout(layout_right, 1)

        widget = QWidget()
        widget.setLayout(layout_t)

        self.setCentralWidget(widget)

    def update_plot(self):
        points = self.optimizer.get_points()
        self.i += 1
        if self.i >= len(points):
            self.i = 0
        point_current = points[self.i]

        self.canvas.ax_1.clear()
        if self.canvas.cbar_1:
            self.canvas.cbar_1.remove()

        self.canvas.ax_1.set_xlim(self.optimizer.get_x_min_max())
        self.canvas.ax_1.set_ylim(self.optimizer.get_y_min_max())
        self.canvas.ax_1.set_xlabel('Компонента A1')
        self.canvas.ax_1.set_ylabel('Компонента A2')
        self.canvas.ax_1.set_title('График линии равных значений объема расхода компонентов')
        self.canvas.ax_1.plot(self.optimizer.get_min_point().x, self.optimizer.get_min_point().y,
                              color='gray', marker='o', label='Найденный максимум')
        cntr = self.canvas.ax_1.contourf(*self.optimizer.get_limits(), levels=50, cmap=cm.coolwarm)
        self.canvas.cbar_1 = self.canvas.fig.colorbar(cntr)

        self.canvas.ax_1.plot([point_current[0][0], point_current[1][0], point_current[2][0], point_current[0][0]],
                              [point_current[0][1], point_current[1][1], point_current[2][1], point_current[0][1]],
                              color='red', label='Текущая итерация (симплекс)')

        self.canvas.ax_1.legend()

        self.canvas.draw()

    def plot_3d(self):
        if self.canvas.cbar_2:
            self.canvas.cbar_2.remove()
        surf = self.canvas.ax_2.plot_surface(*self.optimizer.get_limits(), cmap=cm.coolwarm, antialiased=True)
        self.canvas.ax_2.set_zlim(self.optimizer.get_z_min_max())

        if self.minimum_point_3d:
            self.minimum_point_3d.remove()

        self.minimum_point_3d = self.canvas.ax_2.scatter(
            self.optimizer.get_min_point().x, self.optimizer.get_min_point().y, self.optimizer.get_min_value(),
            color='black', marker='o', label='Найденный максимум')

        self.canvas.ax_2.set_xlim(self.optimizer.get_x_min_max())
        self.canvas.ax_2.set_ylim(self.optimizer.get_y_min_max())
        self.canvas.ax_2.set_title('График зависимости объема расхода от компонентов A1 и A2')
        self.canvas.ax_2.set_xlabel('Компонент A1')
        self.canvas.ax_2.set_ylabel('Компонент A2')
        self.canvas.ax_2.set_zlabel('Расход компонента за смену')
        self.canvas.ax_2.legend()

        self.canvas.cbar_2 = self.canvas.fig.colorbar(surf, fraction=0.03, pad=0.1)
        self.canvas.draw()

    def _open_dialog_info(self):
        dlg = qDialogInfo.QDialogInfo(self)
        dlg.setWindowTitle("Формулировка задачи")
        dlg.exec()

    def _change_user(self):
        self.login_window = qLoginWindow.LoginWindow()
        self.login_window.show()
        self.close()

    # TODO: добавить формализированное описание задания
    # TODO: симплекс метод - добавить методов
    
    def _start_clicked(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        count_iteration = self._get_count_iteration()
        self.optimizer = Optimizer(max_iter=count_iteration)
        self.update_plot()
        self.plot_3d()
        self.founded_optimum_point.setText('Точка минимума: ' + repr(self.optimizer.get_min_point()))
        self.founded_optimum_value.setText(f'Найденный минимум: {self.optimizer.get_min_value():.2f}')

    def _get_count_iteration(self):
        return int(self.input_count_iteration.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserWindow()
    window.show()

    app.exec()
