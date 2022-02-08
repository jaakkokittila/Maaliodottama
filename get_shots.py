import requests
import csv
import pandas as pd

seasons = ['2018', '2019', '2020', '2021', '2022']

def get_shots():
    try:
        return pd.read_csv('data/shots.csv')
    except:
        return None

def check_if_match_is_saved(match_id, shots):
    if shots is None:
        return False
    else:
        return len(shots[shots['Match_id'] == int(match_id)]) > 0

saved_shots = get_shots()

if saved_shots is None:
    write_mode = 'w'
else:
    write_mode = 'a'

field_names = ['Match_id', 'Type', 'Time', 'Shooting_team', 'Left_team', 'Right_team', 'Period', 'Shot_x', 'Shot_y', 'Blocker', 'Shooter', 'Event_type']
with open('data/shots.csv', mode=write_mode) as shot_file:
    shot_writer = csv.DictWriter(shot_file, fieldnames=field_names)

    if write_mode == 'w':
        shot_writer.writeheader()

    for season in seasons:
        url = url='https://liiga.fi/api/v1/games?tournament=runkosarja&season=' + season
        request = requests.get(url)

        matches = request.json()
        match_ids = []

        for match in matches:
            if match['ended'] == True:
                match_ids.append(match['id'])

        for match_id in match_ids:
            match_id_with_season = str(match_id) + str(season)
            match_saved = check_if_match_is_saved(match_id_with_season, saved_shots)

            if match_saved == False:
                shot_base_url = 'https://liiga.fi/api/v1/shotmap/'
                match_shot_url = shot_base_url + season + '/' + str(match_id)

                shot_data = requests.get(match_shot_url)
                match_shots = shot_data.json()

                for shot in match_shots:
                    event_type = shot['eventType']

                    if event_type != 'PLAYER_BLOCKED':
                        shot_type = shot['type']
                        shooting_team = shot['shootingTeamId']
                        left_team = shot['leftTeam']
                        right_team = shot['rightTeam']
                        period = shot['period']
                        shot_x = shot['shotX']
                        shot_y = shot['shotY']
                        time = shot['gameTime']
                        blocker = shot['blockerId']
                        shooter = shot['shooterId']

                        shot_writer.writerow({'Match_id': match_id_with_season, 'Type': shot_type, 'Shooting_team': shooting_team, 'Left_team': left_team, 'Right_team': right_team,
                                              'Period': period, 'Shot_x': shot_x, 'Shot_y': shot_y, 'Time': time, 'Blocker': blocker, 'Shooter': shooter, 'Event_type': event_type})

    shot_file.close()


