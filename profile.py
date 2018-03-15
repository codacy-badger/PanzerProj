from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import hashlib
import re

from models import User, select, session
from config import connection, or_


class UserProfile(Screen):
    source = 'img/icon_profile.png'
    print(StringProperty())
    username = StringProperty()
    print(username)
    # проверка наличия юзера с подобным логином/мэйлом в БД
    def get_user_data(self, username):
        print(username)

