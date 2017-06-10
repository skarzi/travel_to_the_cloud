from flask import Flask
from flask_restful import Api


def init_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    app.config['ALLOWED_EXTENSIONS'] = set(['json', 'amr'])
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
    api = Api(app)
    app.api = api
    add_resources(api)
    return app


def add_resources(api):
    from .resources import SilentLanguage
    api.add_resource(SilentLanguage, '/')
