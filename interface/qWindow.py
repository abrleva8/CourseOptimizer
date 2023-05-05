import sys

from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QGridLayout
from PyQt6.QtWidgets import QToolBar

from interface import qDialogInfo
from function import my_function
from matplotlib import cm

import matplotlib

from plotting.mpl_canvas import MplCanvas

matplotlib.use('QtAgg')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Курсовая работа, 1 вариант")
        self.showMaximized()
        self._add_components()

        # TODO: сделать рефакторинг
        self.i = 0
        self.f = my_function.Function()
        self.f.nelder_mead()

        self.x, self.y = self.f.limits()
        self.z = self.f.calculate((self.x, self.y))
        self.points = self.f.triangle_points

        self.show()

    def _add_components(self):

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Информация", self)
        button_action.setToolTip("Формулировка задачи курсового проекта")
        button_action.triggered.connect(self._open_dialog_info)
        toolbar.addAction(button_action)

        self.ok_button = QPushButton("Нарисовать графики", self)
        # self.ok_button.move(150, 150)
        self.ok_button.clicked.connect(self._start_clicked)
        self.ok_button.setEnabled(True)

        self.canvas = MplCanvas(width=5, height=4, dpi=100)

        layout = QGridLayout()
        layout.addWidget(self.ok_button, 0, 0)
        layout.addWidget(self.canvas, 0, 1, 6, 5)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def update_plot(self):
        points = self.points
        self.i += 1
        if self.i >= len(self.points):
            self.i = 0
        point_current = points[self.i]

        self.canvas.ax_1.clear()
        if self.canvas.cbar:
            self.canvas.cbar.remove()

        self.canvas.ax_1.set_xlim([0.99, 7.05])
        self.canvas.ax_1.set_ylim([0.99, 7.05])
        cntr = self.canvas.ax_1.contourf(self.x, self.y, self.z, levels=50, cmap='RdGy')
        self.canvas.cbar = self.canvas.fig.colorbar(cntr)

        self.canvas.ax_1.plot([point_current[0][0], point_current[1][0], point_current[2][0], point_current[0][0]],
                              [point_current[0][1], point_current[1][1], point_current[2][1], point_current[0][1]], color='red')

        self.canvas.draw()

    def plot_3d(self):
        if self.canvas.cbar_2:
            self.canvas.cbar_2.remove()
        surf = self.canvas.ax_2.plot_surface(self.x, self.y, self.z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
        self.canvas.ax_2.set_zlim(self.z.min(), self.z.max())
        self.canvas.ax_2.set_xlim(self.x.min(), self.x.max())
        self.canvas.ax_2.set_ylim(self.y.min(), self.y.max())
        self.canvas.cbar_2 = self.canvas.fig.colorbar(surf, fraction=0.046, pad=0.04)

    def _open_dialog_info(self):
        dlg = qDialogInfo.QDialogInfo(self)
        dlg.setWindowTitle("Формулировка задачи")
        dlg.exec()

    def _start_clicked(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.update_plot()
        self.plot_3d()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
