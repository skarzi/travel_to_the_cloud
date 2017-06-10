import uuid

import wit
import ffmpy
import requests
import werkzeug

from flask_restful import (
    reqparse,
    Resource
)

from .silent_language import text_to_silent_language_converter

wit_client = wit.Wit(access_token='GNEKSIPCTVCBTRPT2NDVNXXBLPBLNM24')


class SilentLanguage(Resource):
    def __init__(self):
        self._parser = reqparse.RequestParser()
        # self._parser.add_argument('text', type=str, required=False, location='json')
        self._parser.add_argument(
            'audio',
            type=werkzeug.datastructures.FileStorage,
            location='files',
        )

    def post(self):
        args = self._parser.parse_args()
        print("ARGS = ", args)
        audio = args['audio']
        print(audio)
        text = audio_to_text(audio)
        clip_location = text_to_silent_language_converter.convert(text)
        return {'clip_location': clip_location}


def audio_to_text(audio):
    fname = uuid.uuid4()
    audio.save('/tmp/uploads/{0}.amr'.format(fname))
    try:
        ff = ffmpy.FFmpeg(
            inputs={'/tmp/uploads/{0}.amr': None},
            outputs={'/tmp/wavs/{0}.wav'.format(fname): None}
        )
        ff.run()
        data = open('/tmp/wavs/{0}.wav'.format(fname), 'rb').read()
    except Exception as e:
        print(e)

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

    print(response)
    print(response.json())

    if response.status_code == 200:
        body = response.json()
        return body['text_']
    else:
        return None
