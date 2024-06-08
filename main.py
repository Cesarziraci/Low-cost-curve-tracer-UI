from kivymd.app import MDApp
from UI.screen import UI
from utils import RealTimeGraph
from kivy.clock import Clock
from utils import Data
from UI.dialogs import CustomDialog
from Serial_communication.Serial_port import get, write, ser
import threading

x = threading.Thread(target=get, args=(1,))

class Main(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = UI()
        self.graph = RealTimeGraph(title='Characteristic curve', xlabel='V', ylabel='A')
         

    def on_start(self):
        graph_box = self.sm.current_screen.ids.graph_box
        graph_box.add_widget(self.graph.set_graph(0.35))
        Clock.schedule_interval(self.update_graph, 0.1)
        return super().on_start()

    def on_stop(self):
        ser.close()
        return super().on_stop()

    def update_graph(self, dt):
        self.graph.update(Data.Voltage, Data.Current)

        try:
            average_current = sum(Data.Current) / len(Data.Current)
            average_voltage = sum(Data.Voltage) / len(Data.Voltage)
            beta = average_current/Data.beta
        except Exception:
            average_current = 0
            average_voltage = 0
            beta = 0

        self.sm.current_screen.ids.label_2.text = str(average_current)
        self.sm.current_screen.ids.label_4.text = str(average_voltage)
        self.sm.current_screen.ids.label_6.text = str(beta)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        return self.sm
    
    def buttom_callback(self, Type):
        match Type:
            case 'OFF':
                write('OFF')
                CustomDialog('Set', 'Setting Off').open()
            case 'DIODE':
                self.graph.clear()
                CustomDialog('Set', 'Characterizing diode').open()
                write('ENCENDIDO;DIODE')
            case 'MN':
                self.graph.clear()
                CustomDialog('Set', 'Characterizing Mosfet-N').open()
                write('ENCENDIDO;NMOS')
            case 'MP':
                self.graph.clear()
                write('ENCENDIDO;PMOS')
                CustomDialog('Set', 'Characterizing Mosfet-P').open()
            case 'BP':
                self.graph.clear()
                write('ENCENDIDO;BJTP')
                CustomDialog('Set', 'Characterizing BJT-p').open()
            case 'BN':
                self.graph.clear()
                write('ENCENDIDO;BJTN')
                CustomDialog('Set', 'Characterizing BJT-N').open()
            case 'JP':
                self.graph.clear()
                write('ENCENDIDO;PFET')
                CustomDialog('Set', 'Characterizing JFET-P').open()
            case 'JN':
                self.graph.clear()
                write('ENCENDIDO;NFET')
                CustomDialog('Set', 'Characterizing JFET-N').open()
        
if __name__ == '__main__':
    Main().run() 
    x.start()