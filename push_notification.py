from app.push_notification_client import IonicApiClient

if __name__ == '__main__':
    ionic_client = IonicApiClient.from_file('api_key.json')
    ionic_client.push_notification('Jesteś wzywany do kontroli.')
