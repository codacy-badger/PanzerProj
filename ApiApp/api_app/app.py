import falcon

from mobile.web_api import UserInfo, NewUserCreating

api = application = falcon.API()

api.add_route('/user_base_info/{user_id:int}', UserInfo())
api.add_route('/new_user_creating/{user_info}', NewUserCreating())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, api)
    server.serve_forever()
