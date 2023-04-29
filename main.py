from interface import qWindow, qLoginWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    # f = Function()
    # f.plot()
    # f.plot_contours()
    # f.nelder_mead()
    # f.xxx()
    app = QApplication(sys.argv)

    # window = qWindow.MainWindow()
    window = qLoginWindow.LoginWindow()
    window.show()

    app.exec()
