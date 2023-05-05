import sys

from PyQt6.QtWidgets import QApplication

from interface import qLoginWindow

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
