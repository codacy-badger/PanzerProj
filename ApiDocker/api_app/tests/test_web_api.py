import requests


class TestUrls(object):
    def setup_class(self):
        self.sess = requests.Session()

    # проверяем на доступность все возможные урлы
    def test_web_api_routs(self):
        doc = {"images": [{"href": "/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png"}]}

        routs = ['/received_data', '/search_data', '/send_mail', '/change_info', '/main']
        for rout in routs:
            response = self.sess.post(f'http://127.0.0.1:8000{rout}').json()

            assert response == doc

    # проверяем корректность ответа при неверном урле
    def test_invalid_routs(self):
        response = self.sess.post(f'http://127.0.0.1:8000/invalid_url').status_code

        assert response == 404

