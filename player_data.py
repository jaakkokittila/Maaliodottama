import csv
import utilities as utils

player_field_names = ['Id', 'Team', 'Birthday', 'Name', 'Nationality', 'Position', 'Handedness', 'Height', 'Weight', 'Number']

def check_and_add_missing_players(players):
    player_file_path = 'data/players.csv'
    saved_players = utils.read_dataframe(player_file_path, 'cp1252')

    if saved_players is None:
        write_mode = 'w'
    else:
        write_mode = 'a'

    with open(player_file_path, mode=write_mode, encoding='cp1252') as players_file:
        player_writer = csv.DictWriter(players_file, fieldnames=player_field_names)

        if saved_players is None:
            player_writer.writeheader()

        for player in players:
            player_exists = utils.check_if_row_in_dataframe(player['id'], saved_players)

            if player_exists == False:
                team_name = player['teamId'].split(':')[1].upper()
                player_name = player['firstName'] + ' ' + player['lastName']
                player_writer.writerow({'Id': player['id'], 'Team': team_name, 'Birthday': player['dateOfBirth'], 'Name': player_name,
                                        'Nationality': player['nationality'],'Position': player['role'], 'Handedness': player['handedness'],
                                        'Height': player['height'], 'Weight': player['weight']})

        players_file.close()