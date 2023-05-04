import sys

from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWidgets import QToolBar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from interface import qDialogInfo
from logic import my_function
from matplotlib.figure import Figure

import matplotlib

matplotlib.use('QtAgg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=400):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(121)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Курсовая работа, 1 вариант")
        self.resize(1000, 700)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Информация", self)
        button_action.setToolTip("Формулировка задачи курсового проекта")
        button_action.triggered.connect(self._open_dialog_info)
        # button_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)
        self.i = 0
        f = my_function.Function()
        f.nelder_mead()

        self.x, self.y = f.limits()
        self.z = f.calculate((self.x, self.y))
        self.points = f.triangle_points

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.update_plot()
        self.show()

    def update_plot(self):
        points = self.points
        self.i += 1
        if self.i >= len(self.points):
            self.i = 0
        point_0 = points[self.i]
        # self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # Clear the canvas.
        # self.canvas.figure.remove()
        self.canvas.axes.set_xlim([0.99, 7.05])
        self.canvas.axes.set_ylim([0.99, 7.05])

        self.canvas.axes.contour(self.x, self.y, self.z, levels=20, linewidths=0.5, colors='k')
        cntr = self.canvas.axes.contourf(self.x, self.y, self.z, levels=20, cmap="RdBu_r")
        # TODO: подумать как убрать костыль
        if not cntr:
            self.canvas.fig.colorbar(cntr, ax=self.canvas.axes, use_gridspec=False)
        # self.canvas.fig.colorbar(cntr, ax=self.canvas.axes, use_gridspec=None)
        self.canvas.axes.plot([point_0[0][0], point_0[1][0], point_0[2][0], point_0[0][0]],
                              [point_0[0][1], point_0[1][1], point_0[2][1], point_0[0][1]], color='red')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def _open_dialog_info(self, s):
        dlg = qDialogInfo.QDialogInfo(self)
        dlg.setWindowTitle("Формулировка задачи")
        dlg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
