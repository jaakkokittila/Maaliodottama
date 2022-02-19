import requests
import csv
import player_data as player_data
import utilities as utils
import sys

basic_api_base_url = 'https://liiga.fi/api/v1/games/'
detailed_api_base_url = 'https://liiga.fi/api/v1/games/stats/'

def get_match_basic_data(game_id, season, team_type):
    request_url = basic_api_base_url + season + '/' + str(game_id)
    request = requests.get(request_url)

    data = request.json()
    match = data['game']

    team = match[team_type]
    team_id = team['teamId'].split(':')[0]
    team_name = team['teamId'].split(':')[1].upper()
    score = team['goals']
    team_players = data[team_type + 'Players']

    if team_type == 'homeTeam':
        ending_type = match['finishedType']
        date = match['start']

        return team_id, team_name, score, team_players, ending_type, date
    else:
        return team_id, team_name, score, team_players


def write_matches(game_ids, season):
    match_file_path = 'data/matches.csv'
    saved_matches = utils.read_dataframe(match_file_path, 'cp1252')

    if saved_matches is None:
        write_mode = 'w'
    else:
        write_mode = 'a'

    with open(match_file_path, mode=write_mode, encoding='cp1252') as match_file:
        field_names = ['Id', 'Home_id', 'Home_name', 'Away_id', 'Away_name',
                       'Home_score', 'Away_score', 'Ending_type', 'Date', 'Home_players', 'Away_players']
        match_writer = csv.DictWriter(match_file, fieldnames=field_names)

        if saved_matches is None:
            match_writer.writeheader()

        for game_id in game_ids:
            match_id = str(game_id) + str(season)
            matchexists = utils.check_if_row_in_dataframe(match_id, saved_matches)

            if matchexists == False:
                home_id, home_name, home_score, home_players, ending_type, date = get_match_basic_data(game_id, season, 'homeTeam')
                away_id, away_name, away_score, away_players, = get_match_basic_data(game_id, season, 'awayTeam')

                player_data.check_and_add_missing_players(home_players + away_players)

                home_player_ids = ''
                away_player_ids = ''

                for player in home_players:
                    home_player_ids += str(player['id']) + ' '
                for player in away_players:
                    away_player_ids += str(player['id']) + ' '

                match_writer.writerow({'Id': match_id, 'Home_id': home_id, 'Home_name': home_name,
                                       'Away_id': away_id, 'Away_name': away_name, 'Home_score': home_score,
                                       'Away_score': away_score, 'Ending_type': ending_type, 'Date': date,
                                       'Home_players': home_player_ids, 'Away_players': away_player_ids})
        match_file.close()

url='https://liiga.fi/api/v1/games?tournament=runkosarja&season='

#Season argument should be first in command line
season = sys.argv[1]
request = requests.get(url + season)

match_ids = utils.get_match_ids(season)

write_matches(match_ids, season)


