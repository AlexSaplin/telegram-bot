import json

import requests
from pymongo import MongoClient

from src import config
from src.config import MONGO_URL
from src.models import Player, PlayerStats

import dns


class APIInterfaceError(Exception):
    pass


class UnexpectedStatusError(APIInterfaceError):
    pass


class BadResponseError(APIInterfaceError):
    pass


class NotFoundError(APIInterfaceError):
    pass


class StatsAPIInterface:
    def __init__(self):
        self.url = config.STATS_URL
        self.client = MongoClient(MONGO_URL)
        self.db = self.client.NHL
        self.players = self.db.Players

    def get_player(self, player_id):
        return Player.from_dict(self.do_request(endpoint='api/v1/people/{}'.format(player_id))['people'][0])

    def get_player_by_name(self, name):
        result = self.players.find_one({'name': name})
        if result is None:
            raise NotFoundError('There is no player with such name')
        return self.get_player(result['player_id'])

    def get_player_id_by_name(self, name):
        result = self.players.find_one({'name': name})
        if result is None:
            raise NotFoundError('There is no player with such name')
        return result['player_id']

    def get_season_roster(self, season_begging_year):
        params = {
            'expand': 'team.roster',
            'season': f'{season_begging_year}{season_begging_year + 1}'
        }
        return self.do_request(endpoint='api/v1/teams', params=params).get('teams', 'None')

    def get_player_stats(self, player_name: str, season: int):
        game_id = 1
        player_id = f'ID{self.get_player_id_by_name(player_name)}'
        player_stats = {
            'points': 0,
            'assists': 0,
            'goals': 0,
            'plusminus': 0
        }
        while True:
            try:
                result = self.do_request(endpoint=f'api/v1/game/{season}02{game_id:04d}/boxscore')
            except Exception as e:
                break
            result = result.get('teams', {})
            for team_type in ['home', 'away']:
                stats = result.get(team_type, {}).get('players', {}).get(player_id, {}).get('stats', {}).get(
                    'skaterStats', {})
                for stat in player_stats:
                    player_stats[stat] += stats.get(stat, 0)
            player_stats['points'] = player_stats['goals'] + player_stats['assists']
            if result.get('home', None) is None:
                break
            game_id += 1
        return PlayerStats.from_dict(player_stats)

    def do_request(self, endpoint: str, params: dict = None, method: str = 'GET'):
        if not params:
            params = {}

        url = '{}/{}'.format(self.url, endpoint)
        resp = requests.request(url=url, method=method, params=params)
        if resp.status_code != 200:
            response = json.loads(resp.text)
            error = response['message']
            raise UnexpectedStatusError(
                "Code {:d} returned for {} {} endpoint.\n"
                "Error: {}".format(resp.status_code, method, endpoint, error))
        try:
            return json.loads(resp.text)
        except json.JSONDecodeError:
            raise BadResponseError("Failed to parse response"
                                   "Code {:d} returned for {} {} endpoint.".format(resp.status_code, method, endpoint))
