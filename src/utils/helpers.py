from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from utils.constants import Data

class RealTimeGraph:
    def __init__(self,title,xlabel,ylabel, **kwargs):
        super().__init__(**kwargs)
        self.fig, self.ax = plt.subplots(figsize=(8,5))
        self.ax.set_title(title, size = 20)
        self.ax.set_xlabel(xlabel, size = 12)
        self.ax.set_ylabel(ylabel, size = 12, rotation = 90)
        self.data_x = []
        self.data_y = []
        self.buffer_size = 1000
        self.line, = self.ax.plot([], [], 'ro', markersize=4) 
        self.canvas = FigureCanvasKivyAgg(self.fig, size_hint=(1,1))

    def set_graph(self, grid):
        self.ax.grid(alpha = grid)
        return self.canvas

    def update(self, new_x_values, new_y_values): 
        # Extender los datos con los nuevos valores
        self.data_x.extend(new_x_values)
        self.data_y.extend(new_y_values)

        # Limitar el tamaño de los datos al tamaño del buffer (FIFO)
        if len(self.data_x) > self.buffer_size:
            self.data_x = self.data_x[-self.buffer_size:]  # Mantener solo los últimos valores
            self.data_y = self.data_y[-self.buffer_size:]

        # Actualizar los datos de la línea (conectar puntos)
        self.line.set_xdata(self.data_x)
        self.line.set_ydata(self.data_y)

        # Ajustar los límites del gráfico
        self.ax.set_ylim(0,15)
        self.ax.set_xlim(0,2.5)

        # Redibujar el gráfico
        self.canvas.draw()

    def clear(self):
        Data.Current = []
        Data.Voltage = []
        self.data_x = []
        self.data_y = []
        self.line.set_xdata([])
        self.line.set_ydata([])
        self.canvas.draw()