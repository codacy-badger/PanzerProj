import falcon

from web import Resource

api = application = falcon.API()

main = Resource()

api.add_route('/main', main)
api.add_route('/received_data', main)
api.add_route('/search_data', main)
api.add_route('/send_mail', main)
api.add_route('/change_info', main)

