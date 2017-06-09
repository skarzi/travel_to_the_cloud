from flask import Flask
from flask_restful import Api

def init_app():
    app = Flask(__name__)
    api = Api(app)
    app.api = api
    add_resources(api)
    return app


def add_resources(api):
    from .resources import SilentLanguage
    api.add_resource(SilentLanguage, '/')
