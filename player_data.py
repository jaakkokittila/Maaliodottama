import csv
import pandas as pd

player_field_names = ['Id', 'Team', 'Birthday', 'Name', 'Nationality', 'Position', 'Handedness', 'Height', 'Weight', 'Number']

def get_players(player_file_path):
    #Open player-data file to check if player exists in file
    try:
        return pd.read_csv(player_file_path, encoding='cp1252')
    except:
        return None

def player_exists(player, saved_players):
    if saved_players is None:
        return []
    else:
        return saved_players[saved_players['Id'] == player['id']]

def check_and_add_missing_players(players):
    player_file_path = 'data/players.csv'
    saved_players = get_players(player_file_path)

    if saved_players is None:
        write_mode = 'w'
    else:
        write_mode = 'a'

    with open(player_file_path, mode=write_mode, encoding='cp1252') as players_file:
        player_writer = csv.DictWriter(players_file, fieldnames=player_field_names)

        if saved_players is None:
            player_writer.writeheader()

        for player in players:
            playerexists = player_exists(player, saved_players)

            if len(playerexists) == 0:
                team_name = player['teamId'].split(':')[1].upper()
                player_name = player['firstName'] + ' ' + player['lastName']
                player_writer.writerow({'Id': player['id'], 'Team': team_name, 'Birthday': player['dateOfBirth'], 'Name': player_name,
                                        'Nationality': player['nationality'],'Position': player['role'], 'Handedness': player['handedness'],
                                        'Height': player['height'], 'Weight': player['weight']})

        players_file.close()