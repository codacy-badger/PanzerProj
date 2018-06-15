import json
import falcon

from .database.models import User


class UserInfo(object):

    def on_get(self, request, response, user_id):
        db_response = User().get_user_base(user_id)

        json_response = {'user':db_response}

        response.body = json.dumps(json_response, ensure_ascii = False)

        if db_response['success']:
            # если ответ получен
            response.status = falcon.HTTP_200
        else:
            response.status = falcon.HTTP_404

class NewUserCreating(object):

    def on_post(self, request, response, user_info):
        db_response = User().create_new_user(new_user_data = user_info)

        json_response = {'result':db_response}

        response.body = json.dumps(json_response, ensure_ascii = False)

        if db_response:
            # если ответ получен
            response.status = falcon.HTTP_200
        else:
            # при ощибке
            response.status = falcon.HTTP_404
