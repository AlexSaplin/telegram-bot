import json

import requests

from src import config


class APIInterfaceError(Exception):
    pass


class UnexpectedStatusError(APIInterfaceError):
    pass


class BadResponseError(APIInterfaceError):
    pass


class StatsAPIInterface:
    def __init__(self):
        self.url = config.STATS_URL
        self.team_id = config.CAPS_ID

    def get_roster(self):
        return self.do_request(endpoint='api/v1/teams/{}/roster'.format(self.team_id))

    def get_player(self, player_id):
        return self.do_request(endpoint='api/v1/people/{}'.format(player_id))

    def do_request(self, endpoint: str, params: dict = None, method: str ='GET'):
        if not params:
            params = {}

        url = '{}/{}'.format(self.url, endpoint)
        resp = requests.request(url=url, method=method, params=params)

        if resp.status_code != 200:
            response = json.loads(resp)
            error = response['error']
            raise UnexpectedStatusError("Code {:d} returned for {} {} endpoint."
                                        "Error: {}".format(resp.status_code, method, endpoint, error))

        try:
            return json.loads(resp.text)
        except json.JSONDecodeError:
            raise BadResponseError("Failed to parse response"
                                   "Code {:d} returned for {} {} endpoint.".format(resp.status_code, method, endpoint))
