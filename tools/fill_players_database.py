from time import sleep

from pymongo import MongoClient

from src import StatsAPIInterface


def fill_players_database():
    client = MongoClient()

    db = client.NHL
    players = db.Players

    current_season = 1917

    stats_interface = StatsAPIInterface()
    while True:
        print(f'Current season: {current_season}/{current_season + 1}')
        try:
            season_roster = stats_interface.get_season_roster(current_season)
        except Exception as e:
            break

        for team in season_roster:
            for player in team.get('roster', {}).get('roster', []):
                players.update_one(
                    filter={'name': player['person']['fullName']},
                    update={'$set': {'player_id': int(player['person']['id'])}},
                    upsert=True
                )

        current_season += 1
        sleep(0.5)


if __name__ == '__main__':
    fill_players_database()
