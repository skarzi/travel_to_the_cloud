import os
import json

import requests

from .silent_language import text_to_silent_language_converter


class IonicApiClient:
    """
    Communicates with external Ionic Cloud Api Services
    """

    API_URL = 'https://api.ionic.io/'

    def __init__(self, api_token=None):
        self._api_token = api_token or os.environ.get('IONIC_API_TOKEN')
        print(self._api_token)
        self.HEADERS = {
            'Authorization': 'Bearer ' + self._api_token,
        }

    @classmethod
    def from_file(cls, fname, key="api_key"):
        with open(fname) as f:
            api_key = json.load(f)[key]
        return cls(api_key)

    def push_notification(self, text):
        try:
            clip_location = text_to_silent_language_converter.convert(text)
        except Exception as e:
            clip_location = None
        json_data = {
            'text': text,
            'clip_location': os.path.basename(clip_location),
        }
        print("DATA", json_data)
        print("sending notification!")
        endpoint = 'push/notifications'
        headers = dict({'Content-Type': 'application/json'}, **(self.HEADERS))
        data = json.dumps({
            'send_to_all': True, 'profile': 'develop',
            'notification': {
                'message': 'Nowe powiadienie!',
                'title': 'Silent Notifier',
                'payload': json_data,
            }
        })
        r = requests.post(self.API_URL + endpoint, headers=headers, data=data)
        print(r)
        print(r.json())
        print(r.status_code)
