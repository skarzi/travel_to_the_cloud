import falcon

from resources import SilentLanguage, VideoProvider

app = falcon.API()

app.add_route('/', SilentLanguage())
app.add_route('/video/{location}/{filename}', VideoProvider())
