from kivymd.app import MDApp
from UI.screen import UI

class Main(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = UI()

    def on_start(self):
        return super().on_start()

    def on_stop(self):
        return super().on_stop()

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        return self.sm
    
    def buttom_callback(self, Type):
        match Type:
            case 'OFF':
                pass
            case 'DIODE':
                pass
            case 'MN':
                pass
            case 'MP':
                pass
            case 'BP':
                pass
            case 'BN':
                pass
            case 'JP':
                pass
            case 'JN':
                pass
        
if __name__ == '__main__':
    Main().run()