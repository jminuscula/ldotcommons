import json

import twitter as twapi
from ldotcommons import logging
from ldotcommons import messaging

_logger = logging.get_logger(__name__)


class Twitter(twapi.Twitter, messaging.Notifier):
    def __init__(self,
                 consumer_key='', consumer_secret='',
                 token='', token_secret=''):
        super(Twitter, self).__init__(auth=twapi.OAuth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            token=token,
            token_secret=token_secret))

    def send(self, msg, detail=''):
        try:
            self.statuses.update(status=msg)
        except twapi.TwitterHTTPError as e:
            response = json.loads(e.response_data.decode('utf-8'))
            for error in response['errors']:
                _logger.error('Error {code}: {message}'.format(
                    code=error['code'],
                    message=error['message']))

    def recv(self, user_name=None, since=None):
        pass
