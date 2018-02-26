from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout

from models import User, select
from config import connection, or_


class MainScreen(FloatLayout):
   def __init__(self, **kwargs):
      super(MainScreen, self).__init__(**kwargs)
      self.add_widget(Label(text='Fuck u:'))
      self.username = TextInput(multiline=True)
      self.add_widget(self.username)

      s = select([User])
      result = connection.execute(s)
      print(result.fetchall())

class NewUserRegistration(FloatLayout):
   def __init__(self, **kwargs):
      super(NewUserRegistration, self).__init__(**kwargs)
      self.add_widget(Label(text='Fuck u:'))
      self.username = TextInput(multiline=True)
      self.add_widget(self.username)
      
   def data_validation(self, username, email, password):
      validation_request = select([User]).where(or_(User.username == username, User.email == email))
      validation_result = connection.execute(validation_request)
      if validation_result:
         return False
      else:
         return True
       
      
class Simple(App):
   def build(self):
      return MainScreen()
   
if __name__ == '__main__':
   x = NewUserRegistration().data_validation(username='dsa', email='dasdas', password='dqwdq')
   print(x)