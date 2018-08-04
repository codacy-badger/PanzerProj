from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import datetime

from ApiApp.api_app import db_name, db_user, db_password

# автоматический сбор инфомрации о таблицах в БД
Base = automap_base()

# подключаемся к БД
engine = create_engine(f'postgresql://{db_user}:{db_password}@localhost:5432/{db_name}')

# получаем схему таблиц в БД
Base.prepare(engine, reflect=True)

class User():
    def __init__(self):
        # подключаемся к таблице с юзерами
        self.auth_user = Base.classes.auth_user
        # создаём сессию для работы
        self.session = Session(engine)
        # результат обработки запроса
        self.result = {}

    # получение базовой информации о пользователе
    def get_user_base(self, id):
        try:
            db_result = self.session.query(self.auth_user).get(id)

            if db_result and db_result.is_active:
                self.result.update({'success': True,
                                    'username':db_result.username,
                                    'email': db_result.email,
                                    'first_name': db_result.first_name,
                                    'last_name': db_result.last_name,
                                    'last_login_date': db_result.last_login.strftime("%d.%m.%Y"),
                                    'last_login_time': db_result.last_login.strftime("%H:%M")})
            else:
                self.result.update({'success': False,
                                    'error': 'no_user'})

        except Exception as err:

            self.result.update({'success': False,
                                'error': err})

        finally:
            return self.result

    # создание нового аккаунта
    def create_new_user(self, new_user_data):
        # проверка наличия пользователя с подобным email и username
        check_response = self.check_user_exist(new_user_data['username'], new_user_data['email'])

        try:
            # если пользователь с таким username/email ещё не существует - создаём
            if check_response['success'] and not check_response['exist']:
                # создаём нового юзера
                self.session.add(self.auth_user(username = new_user_data['username'],
                                                password = new_user_data['password'],
                                                first_name = new_user_data['first_name'],
                                                last_name = new_user_data['last_name'],
                                                email = new_user_data['email'],
                                                is_superuser = False,
                                                is_staff = False,
                                                is_active = False,
                                                date_joined = datetime.datetime.today()))

                self.session.commit()

                self.result.update({'success':True,
                                    'user_id':self.session.query(self.auth_user).
                                    filter(self.auth_user.username==new_user_data['username']).first().id})
            else:
                # возвращается json с текстом ошибки
                self.result.update({'success': False,
                                    'error': 'user_already_exist'})

        except Exception as err:

            self.result.update({'success': False,
                                'error': err})

        finally:
            return self.result

    # проверка наличия юзера в БД
    def check_user_exist(self, username=None, user_mail=None):
        db_username = db_user_mail = None
        try:
            # поиск юзера в бд по username, если был передан
            if username:
                db_username = self.session.query(self.auth_user).filter(self.auth_user.username==username).first()
            # поиск юзера в бд по email, если был передан
            if user_mail:
                db_user_mail = self.session.query(self.auth_user).filter(self.auth_user.email==user_mail).first()
            # если был найден юзер с подобным email или username -
            if db_user_mail or db_username:
                self.result.update({'success':True,
                                    'exist': True})
            else:
                self.result.update({'success':True,
                                    'exist': False})

        except Exception as err:

            self.result.update({'success': False,
                                'error': err})

        finally:
            return self.result

    # удаление юзера из БД
    def delete_user(self, user_id):
        try:
            # удаляем юзера по ID
            self.session.query(self.auth_user).filter(self.auth_user.id==user_id).delete(synchronize_session=False)

            self.session.commit()

            self.result.update({'success':True})

        except Exception as err:

            self.result.update({'success': False,
                                'error': err})

        finally:
            return self.result


    def __del__(self):
        self.session.close()
