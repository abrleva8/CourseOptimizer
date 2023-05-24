import sys

import matplotlib
from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QGridLayout, QLabel, QHBoxLayout, \
    QLineEdit, QComboBox
from PyQt6.QtWidgets import QToolBar
from matplotlib import cm

from interface import qDialogInfo, qLoginWindow, qAdminWindow
from interface.qTableWindow import MyTableView
from logic import Optimizer, AdminWorker
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

        self.label_methods = QLabel("Доступные методы")
        self.methods_combo_box = QComboBox()
        self.methods_combo_box.currentTextChanged.connect(self._method_combo_box_changed)

        self.label_variations = QLabel("Доступные варианты")
        self.variations_combo_box = QComboBox()
        self.variations_combo_box.currentTextChanged.connect(self._variation_combo_box_changed)

        self.label_count_iteration = QLabel("Число итерации")

        self.input_count_iteration = QLineEdit("10")
        self.input_count_iteration.setPlaceholderText('Введите число итерации')
        self.input_count_iteration.setInputMask("d0")

        self.calculate_button = QPushButton("Нарисовать графики", self)
        self.calculate_button.clicked.connect(self._start_clicked)
        self.calculate_button.setEnabled(True)

        self.show_table_button = QPushButton("Показать точки", self)
        self.show_table_button.clicked.connect(self._show_table_clicked)
        self.show_table_button.setEnabled(False)

        self.founded_optimum_point = QLabel("Точка максимума: ", self)
        self.founded_optimum_value = QLabel("Найденный максимум: ", self)
        self.founded_optimum_value_product = QLabel("Максимальный выход целевого\nкомпонента в кг за рабочую смену: ",
                                                    self)
        self.optimum_value_product = QLabel(self)

        self.canvas = MplCanvas(width=4, height=4, dpi=100)

        layout_t = QHBoxLayout(self)

        layout_left = QGridLayout()
        layout_right = QGridLayout()
        layout_left.addWidget(self.label_methods, 0, 0)
        layout_left.addWidget(self.methods_combo_box, 0, 1)
        layout_left.addWidget(self.label_variations, 1, 0)
        layout_left.addWidget(self.variations_combo_box, 1, 1)
        layout_left.addWidget(self.label_count_iteration, 2, 0)
        layout_left.addWidget(self.input_count_iteration, 2, 1)
        layout_left.addWidget(self.calculate_button, 3, 0)
        layout_left.addWidget(self.show_table_button, 4, 0)
        layout_left.addWidget(self.founded_optimum_point, 5, 0)
        layout_left.addWidget(self.founded_optimum_value, 6, 0)
        layout_left.addWidget(self.founded_optimum_value_product, 7, 0)
        layout_left.addWidget(self.optimum_value_product, 7, 1)
        layout_right.addWidget(self.canvas)

        layout_t.addLayout(layout_left, 0)
        layout_t.addLayout(layout_right, 1)

        widget = QWidget()
        widget.setLayout(layout_t)

        self.setCentralWidget(widget)
        self._get_methods()
        self._get_variations()

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
        self.canvas.ax_1.set_title('График линии равных значений выхода продукта')
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
        self.canvas.ax_2.set_title('График зависимости выхода продукта от компонентов A1 и A2')
        self.canvas.ax_2.set_xlabel('Компонент A1')
        self.canvas.ax_2.set_ylabel('Компонент A2')
        self.canvas.ax_2.set_zlabel('Выход компонента за час')
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

    def _show_table_clicked(self):
        data = self.optimizer.get_points()
        self.window = MyTableView(data, self.count_iteration, 3)

    def _start_clicked(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.count_iteration = self._get_count_iteration()
        self.optimizer = Optimizer(max_iter=self.count_iteration)
        self.update_plot()
        self.plot_3d()
        min_value = self.optimizer.get_min_value()
        self.founded_optimum_point.setText('Точка максимума: ' + repr(self.optimizer.get_min_point()))
        self.founded_optimum_value.setText(f'Найденный максимум: {min_value:.2f}')
        self.optimum_value_product.setText(f'{8 * min_value:.2f} кг')
        self.show_table_button.setEnabled(True)

    def _get_count_iteration(self):
        return int(self.input_count_iteration.text())

    def _get_methods(self):
        admin_worker = AdminWorker()
        list_of_methods = admin_worker.get_methods()
        name_of_methods = list(map(lambda x: x[0], list_of_methods))
        self.methods_combo_box.clear()
        self.methods_combo_box.addItems(name_of_methods)

    def _get_variations(self):
        admin_worker = AdminWorker()
        list_of_variations = admin_worker.get_variations()
        name_of_variations = list(map(lambda x: x[0], list_of_variations))
        self.variations_combo_box.clear()
        self.variations_combo_box.addItems(name_of_variations)

    def _method_combo_box_changed(self):
        text = self.methods_combo_box.currentText()
        if text == 'Метод Нелдер - Мида':
            self.calculate_button.setEnabled(True)
        else:
            self.calculate_button.setEnabled(False)

    def _variation_combo_box_changed(self):
        text = self.variations_combo_box.currentText()
        if text == 'Абрамян':
            self.calculate_button.setEnabled(True)
        else:
            self.calculate_button.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserWindow()
    window.show()

    app.exec()
