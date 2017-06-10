import os
import json

import requests


class IonicApiClient:
    """
    Communicates with external Ionic Cloud Api Services
    """

    API_URL = 'https://api.ionic.io/'

    def __init__(self, api_token=None):
        self._api_token = api_token or os.environ.get('IONIC_API_TOKEN')
        self.HEADERS = {
            'Authorization': 'Bearer ' + self._api_token,
        }

    @classmethod
    def from_file(cls, fname, key="api_key"):
        with open(fname) as f:
            api_key = json.load(f)[key]
        return cls(api_key)

    def push_notification(self, call):
        print("sending notification!")
        endpoint = 'push/notifications'
        headers = dict({'Content-Type': 'application/json'}, **(self.HEADERS))
        data = json.dumps({
            'send_to_all': True, 'profile': 'silent-notifier',
            'notification': {
                'message': 'Nowe powiadienie!',
                'title': 'Silent Notifier',
                'payload': call,
            }
        })
        requests.post(self.API_URL + endpoint, headers=headers, data=data)
