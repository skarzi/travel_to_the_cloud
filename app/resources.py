import os
import uuid

import ffmpy
import requests
import werkzeug
import wit
from flask_restful import (
    reqparse,
    Resource
)

from .silent_language import text_to_silent_language_converter

wit_client = wit.Wit(access_token='GNEKSIPCTVCBTRPT2NDVNXXBLPBLNM24')


class SilentLanguage(Resource):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('text', location="json", type=str)
        self._parser.add_argument(
            'audio',
            type=werkzeug.datastructures.FileStorage,
            location='files',
        )

    def post(self):
        args = self._parser.parse_args()
        audio = args['audio']
        text = args['text']
        if audio is not None:
            text = audio_to_text(audio)
        if text is None:
            return {}, 404
        try:
            clip_location = text_to_silent_language_converter.convert(text)
        except Exception as e:
            return {}, 404
        data = {
            'clip_location': os.path.basename(clip_location),
            'text': text,
        }
        return data


def audio_to_text(audio):
    fname = str(uuid.uuid4())
    audio.save('/tmp/uploads/{0}.amr'.format(fname))
    try:
        ff = ffmpy.FFmpeg(
            inputs={'/tmp/uploads/{0}.amr'.format(fname): None},
            outputs={'/tmp/wavs/{0}.wav'.format(fname): None}
        )
        ff.run()
    except Exception as e:
        print(e)
    data = open('/tmp/wavs/{0}.wav'.format(fname), 'rb').read()

    url = 'https://api.wit.ai/speech'

    headers = {
        "Authorization": "Bearer GNEKSIPCTVCBTRPT2NDVNXXBLPBLNM24",
        "Content-Type": "audio/wav"
    }

    response = requests.post(
        url=url,
        data=data,
        headers=headers
    )

    if response.status_code == 200:
        body = response.json()
        return body['_text']
    else:
        return None
