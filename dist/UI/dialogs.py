from kivymd.uix.dialog import MDDialog

class CustomDialog:
    def __init__(self, title, message, buttons=[]):

        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=buttons,
        )

    def open(self):
        self.dialog.open()
    
    def close(self):
        self.dialog.dismiss() 