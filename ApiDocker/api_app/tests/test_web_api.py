import requests

from ApiDocker.api_app.web.database.models import User


class TestRouts(object):
    def setup_class(self):
        self.sess = requests.Session()
        self.test_user_data = {'username': 'TestUsername',
                               'password':'TestPass',
                               'first_name':'TestFirstName',
                               'last_name':'TestLastName',
                               'email': 'test@test.com'}

    # проверяем корректность вывода информации о пользователе
    def test_user_base_info(self):
        # делаем запрос к api для получения информации о юзере
        response = self.sess.get('http://localhost:8000/user_base_info/1')
        # список ожидаемых ключей
        default_keys = ['success','username', 'email', 'first_name', 'last_name', 'last_login_date', 'last_login_time']

        # проверка наличия всех нужных елчюей в ответе сервера
        for key in response.json()['user'].keys():
            assert key in default_keys

        assert response.status_code == 200
        assert response.json()['user']['success']

    # проверяем корректность ответа при неверном id пользователя
    def test_invalid_user_base_info(self):
        response = self.sess.get(f'http://127.0.0.1:8000/user_base_info/0')
        #
        assert response.status_code == 404
        assert not response.json()['user']['success']
        assert response.json()['user']['error'] == 'no_user'


class TestDatabase(object):
    def setup_class(self):
        self.test_user_data = {'username': 'TestUsername',
                               'password':'TestPass',
                               'first_name':'TestFirstName',
                               'last_name':'TestLastName',
                               'email': 'test@test.com'}

    # проверяем создание юзера
    def test_new_user_creating(self):
        new_user = User().create_new_user(new_user_data = self.test_user_data)

        assert new_user['success']

        # проверяем наличие юзера в бд
        existed = User().check_user_exist(user_mail = self.test_user_data['email'],
                                          username = self.test_user_data['username'])

        assert existed['success']
        assert existed['exist']

        # удаляем юзера из бд
        deleted = User().delete_user(user_id = new_user['user_id'])

        assert deleted['success']

        # проверяем отсутствие юзера в бд
        existed = User().check_user_exist(user_mail = self.test_user_data['email'],
                                          username = self.test_user_data['username'])

        assert existed['success']
        assert not existed['exist']
