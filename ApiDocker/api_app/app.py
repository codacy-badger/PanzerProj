import falcon

from web import Resource

app = application = falcon.API()

main = Resource()
app.add_route('/main', main)
