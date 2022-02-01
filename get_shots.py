import requests
import csv

seasons = ['2018', '2019', '2020', '2021', '2022']

field_names = ['Match_id', 'Type', 'Shooting_team', 'Left_team', 'Right_team', 'Period', 'Shot_x', 'Shot_y', 'Blocker', 'Shooter', 'Event_type']
with open('shots.csv', mode='w', encoding='cp1252') as shot_file:
    shot_writer = csv.DictWriter(shot_file, fieldnames=field_names)
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
                    blocker = shot['blockerId']
                    shooter = shot['shooterId']

                    shot_writer.writerow({'Match_id': str (match_id) + str(season), 'Type': shot_type, 'Shooting_team': shooting_team, 'Left_team': left_team, 'Right_team': right_team,
                                          'Period': period, 'Shot_x': shot_x, 'Shot_y': shot_y, 'Blocker': blocker, 'Shooter': shooter, 'Event_type': event_type})

    shot_file.close()


