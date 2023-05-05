from matplotlib import gridspec
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=400):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.gs = gridspec.GridSpec(1, 2)
        self.ax_1 = self.fig.add_subplot(self.gs[0])
        self.ax_2 = self.fig.add_subplot(self.gs[1], projection='3d')
        self.cbar = None
        self.cbar_2 = None
        super(MplCanvas, self).__init__(self.fig)
