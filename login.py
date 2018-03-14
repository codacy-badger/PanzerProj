import kivy
kivy.require("1.10.0")
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

import hashlib

from models import User, select
from config import connection, and_


class Login(Screen):
    def do_login(self, username, password):
        validation_request = select([User]).where(and_(User.username == username, User.password == hashlib.sha256(password.encode('utf-8')).hexdigest()))
        validation_result = connection.execute(validation_request)
        if validation_result.fetchone():
            popup = Popup(title='Success!', content=Label(text='You successfully login!'),
                          size_hint=(None, None), size=(200, 130))
            popup.open()
        else:
            popup = Popup(title='Error!', content=Label(text='Invalid data! Check your username or password!'),
                          size_hint=(None, None), size=(350, 130))
            popup.open()

    def reset_form(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""