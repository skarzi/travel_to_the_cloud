from flask_restful import (
    reqparse,
    Resource
)

from .silent_language import text_to_silent_language_converter


class SilentLanguage(Resource):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('text', type=str, location='json')

    def post(self):
        args = self._parser.parse_args()
        text = args['text']
        clip_location = text_to_silent_language_converter.convert(text)
        return {'clip_location': clip_location}
