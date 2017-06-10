import json
import os

import falcon
from falcon.uri import parse_query_string

from silent_language.converter import text_to_silent_language_converter


class SilentLanguage:
    def on_get(self, request: falcon.Request, response):
        text = parse_query_string(request.query_string)
        text = text.get('text', None)
        if not text:
            raise falcon.HTTP_BAD_REQUEST
        clip_location = text_to_silent_language_converter.convert(text)

        response.body = json.dumps({'clip_location': clip_location})


class VideoProvider:
    def on_get(self, request, response, location, filename):
        path = os.path.join(location, filename)
        print(path)
        response.status = falcon.HTTP_200
        response.content_type = 'video/mp4'
        with open(path, 'rb') as f:
            response.body = f.read()
