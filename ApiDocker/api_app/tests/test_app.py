import msgpack
import requests


class TestClass(object):

    def test_web_api_routs(self):
        self.sess = requests.Session()
        doc = {"images": [{"href": "/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png"}]}

        routs = ['/received_data', '/search_data', '/send_mail', '/change_info', '/main']
        for rout in routs:
            response = self.sess.post(f'http://127.0.0.1:8000{rout}').json()

            assert response == doc



