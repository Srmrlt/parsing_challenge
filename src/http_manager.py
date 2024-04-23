import logging

import requests

logger = logging.getLogger('HTTPSession')


class HTTPSessionManager:
    def __init__(self, url):
        self.url = url
        self.response = None

    def get_data(self):
        headers = {'Accept-Encoding': 'identity'}
        self.response = requests.get(self.url, stream=True, headers=headers)
        logger.info(f"Response status code: {self.response.status_code}")

    def get_raw_response(self):
        return self.response.raw if self.response else None
