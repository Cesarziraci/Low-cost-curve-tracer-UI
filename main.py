from kivymd.app import MDApp
from UI.screen import UI
from utils import RealTimeGraph
from kivy.clock import Clock
from utils import Data
from UI.dialogs import CustomDialog
from Serial_communication.Serial_port import get, write, ser
import threading

class Main(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = UI()
        self.graph = RealTimeGraph(title='Characteristic curve', xlabel='V', ylabel='A')
        self.read_thread = threading.Thread(target=get, daemon=True)
        self.update_event = None
         
    def on_start(self):
        graph_box = self.sm.current_screen.ids.graph_box
        graph_box.add_widget(self.graph.set_graph(0.35))
        if not self.read_thread.is_alive():
            self.read_thread.start()
        return super().on_start()

    def on_stop(self):
        if ser.is_open:
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

        self.sm.current_screen.ids.label_2.text = f"{average_current:.2f}"
        self.sm.current_screen.ids.label_4.text = f"{average_voltage:.2f}"
        self.sm.current_screen.ids.label_6.text = f"{beta:.2f}"

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        return self.sm
    
    def button_callback(self, Type):
        if Type == 'OFF':
            write('OFF')
            CustomDialog('Set', 'Setting Off').open()
            if self.update_event:
                Clock.unschedule(self.update_event)
                self.update_event = None
        else:
            self.graph.clear()
            if not self.update_event:
                self.update_event = Clock.schedule_interval(self.update_graph, 0.1)
            self.graph.clear()

            match Type:
                case 'DIODE':
                    CustomDialog('Set', 'Characterizing diode').open()
                    write('ENCENDIDO;DIODE')
                case 'MN':
                    CustomDialog('Set', 'Characterizing Mosfet-N').open()
                    write('ENCENDIDO;NMOS')
                case 'MP':
                    CustomDialog('Set', 'Characterizing Mosfet-P').open()
                    write('ENCENDIDO;PMOS')
                case 'BP':
                    CustomDialog('Set', 'Characterizing BJT-p').open()
                    write('ENCENDIDO;BJTP')
                case 'BN':
                    CustomDialog('Set', 'Characterizing BJT-N').open()
                    write('ENCENDIDO;BJTN')
                case 'JP':
                    CustomDialog('Set', 'Characterizing JFET-P').open()
                    write('ENCENDIDO;PFET')
                case 'JN':
                    CustomDialog('Set', 'Characterizing JFET-N').open()
                    write('ENCENDIDO;NFET')
        
if __name__ == '__main__':
    Main().run() 