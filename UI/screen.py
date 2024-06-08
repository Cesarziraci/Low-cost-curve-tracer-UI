from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import threading

Builder.load_file("UI/kv/ui.kv")

class UI(MDScreenManager):
    pass

class Principal_Screen(MDScreen):
    pass