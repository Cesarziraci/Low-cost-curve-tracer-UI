from kivymd.app import MDApp


class Main(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_start(self):
        return super().on_start()

    def on_stop(self):
        return super().on_stop()

    def build(self):
        return super().build()

if __name__ == '__main__':
    Main.run()