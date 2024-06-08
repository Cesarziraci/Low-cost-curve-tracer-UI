from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from utils.constants import Data

class RealTimeGraph:
    def __init__(self,title,xlabel,ylabel, **kwargs):
        super().__init__(**kwargs)
        self.fig, self.ax = plt.subplots(figsize=(8,5))
        self.ax.set_title(title, size = 20)
        self.ax.set_xlabel(xlabel, size = 10)
        self.ax.set_ylabel(ylabel, size = 10)
        self.data_x = []
        self.data_y = []
        self.line, = self.ax.plot([], [], color='red', markersize=1, linewidth=1)
        self.canvas = FigureCanvasKivyAgg(self.fig, size_hint=(1,1))

    def set_graph(self, grid):
        self.ax.grid(alpha = grid)
        return self.canvas

    def update(self, new_x_value, new_y_value):
        
        self.data_x.append(new_x_value)
        self.data_y.append(new_y_value)

        self.line.set_xdata(self.data_x)
        self.line.set_ydata(self.data_y)

        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw()

    def clear(self):
        Data.Current = []
        Data.Voltage = []
        self.data_x = []
        self.data_y = []
        self.line.set_xdata([])
        self.line.set_ydata([])
        self.canvas.draw()