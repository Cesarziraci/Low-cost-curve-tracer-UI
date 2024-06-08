from kivymd.app import MDApp
from UI.screen import UI
from utils import RealTimeGraph
from kivy.clock import Clock
from utils import Data
import random

class Main(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = UI()
        self.graph = RealTimeGraph(title='Characteristic curve', xlabel='V', ylabel='A')

    def on_start(self):
        graph_box = self.sm.current_screen.ids.graph_box
        graph_box.add_widget(self.graph.set_graph(0.35))
        Clock.schedule_interval(self.update_graph, 0.01)
        return super().on_start()

    def update_graph(self, dt):
        Data.Current = random.uniform(0, 10)
        Data.Voltage = random.uniform(5, 10)
        self.graph.update(Data.Voltage, Data.Current)

        self.sm.current_screen.ids.label_2.text = str(Data.Voltage)
        self.sm.current_screen.ids.label_4.text = str(Data.Current)
        self.sm.current_screen.ids.label_6.text = '12'

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        return self.sm
    
    def buttom_callback(self, Type):
        match Type:
            case 'DIODE':
                self.graph.clear()
            case 'MN':
                self.graph.clear()
            case 'MP':
                self.graph.clear()
            case 'BP':
                self.graph.clear()
            case 'BN':
                self.graph.clear()
            case 'JP':
                self.graph.clear()
            case 'JN':
                self.graph.clear()
        
if __name__ == '__main__':
    Main().run()