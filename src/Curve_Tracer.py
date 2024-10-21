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
        self.graph = RealTimeGraph(title='Characteristic curve', xlabel='V', ylabel='mA')
        self.read_thread = None  # No se inicia aún
        self.update_event = None
         
    def on_start(self):
        graph_box = self.sm.current_screen.ids.graph_box
        graph_box.add_widget(self.graph.set_graph(0.50))
        return super().on_start()

    def on_stop(self):
        if ser.is_open:
            ser.close()
        return super().on_stop()

    def update_graph(self, dt):
        min_length = min(len(Data.Voltage), len(Data.Current))
        voltage = Data.Voltage[:min_length]
        current = Data.Current

        self.graph.update(Data.Voltage, Data.Current)

        try:
            average_current = sum(current) / len(Data.Current)
            average_voltage = sum(voltage) / len (Data.Voltage)
            beta = average_current*1000/Data.beta
        except Exception:
            average_current = 0
            average_voltage = 0
            beta = 0

        self.sm.current_screen.ids.label_2.text = f"{average_voltage:.2f} V"
        self.sm.current_screen.ids.label_4.text = f"{average_current:.3f} mA"
        self.sm.current_screen.ids.label_6.text = f"{beta:.2f}"

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        self.title = 'Curve Tracer'
        return self.sm
    
    def button_callback(self, Type):
        if Type == 'OFF':
            write('OFF')
            CustomDialog('Set', 'Setting Off').open()
            if self.update_event:
                Clock.unschedule(self.update_event)
                self.update_event = None
            ser.close()
        else:
            if not ser.is_open:
                ser.open()  # Asegura que el puerto esté abierto
            self.graph.clear()
            if not self.update_event:
                self.update_event = Clock.schedule_interval(self.update_graph, 0.01)

            # Iniciar el hilo de lectura si no está corriendo
            if self.read_thread is None or not self.read_thread.is_alive():
                self.read_thread = threading.Thread(target=get, daemon=True)
                self.read_thread.start()

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