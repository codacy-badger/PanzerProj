from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import hashlib
import re

from models import User, select, session
from config import connection, or_


class NewUserRegistration(Screen):
    # проверка наличия юзера с подобным логином/мэйлом в БД
    def data_validation(self, username, email, first_name, last_name, password_second, password_first):
        # проверка на валидность паролей
        if password_first == password_second:
            # выборка юзеров по логину/мэйлу из БД
            validation_request = select([User]).where(or_(User.username == username, User.email == email))
            validation_result = connection.execute(validation_request)
            if validation_result.fetchall():
                self.manager.current = 'registration'
                popup = Popup(title='Error!', content=Label(text='Username or E-Mail already in use!'),
                              size_hint=(None, None), size=(260, 130))
                popup.open()
            else:
                # проверка введённых данных
                if len(username) > 3 and re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) and\
                   len(first_name) > 3 and len(last_name) > 3 and len(password_first) > 6:
                    # создание нового юзера
                    new_user = User(username=username,
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    password=hashlib.sha256(password_first.encode('utf-8')).hexdigest())
                    s = session()
                    s.add(new_user)
                    s.commit()
                    self.manager.current = 'login'

                    popup = Popup(title='Success!', content=Label(text='Check your e-mail!'),
                                  size_hint=(None, None), size=(200, 130))
                    popup.open()
                else:
                    popup = Popup(title='Error!', content=Label(text='Invalid data! Check registration form!'),
                                  size_hint=(None, None), size=(270, 130))
                    popup.open()
        else:
            self.manager.current = 'registration'
            popup = Popup(title='Error!', content=Label(text='Not similar passwords!'),
                          size_hint=(None, None), size=(200, 130))
            popup.open()
