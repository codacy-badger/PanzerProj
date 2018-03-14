from kivy.app import App
import kivy
kivy.require("1.10.0")
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder

import os
from models import User, select
from config import connection, or_, and_


from connected import Connected
from registration import NewUserRegistration
from login import Login

# load .kv files
Builder.load_file('kv_files/login_page.kv')


class MainApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        manager.add_widget(NewUserRegistration(name='registration'))

        return manager






if __name__ == '__main__':
    MainApp().run()
