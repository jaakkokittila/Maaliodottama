import pandas as pd

shots = pd.read_csv('data/shots.csv', encoding='cp1252')

def transform_coordinates_to_one_end(match_shots):
    left_team_id = match_shots.iloc[0]['Left_team']
    right_team_id = match_shots.iloc[0]['Right_team']

    for i, row in match_shots.iterrows():
        if row['Shooting_team'] == left_team_id and (row['Period'] == 1 or row['Period'] == 3) or row['Shooting_team'] == right_team_id and row['Period'] == 2:
            new_x = -1 * (row['Shot_x'] - 1030)
            shots.loc[i, 'Shot_x'] = new_x
            new_y = -1 * (row['Shot_y'] - 515)
            shots.loc[i, 'Shot_y'] = new_y

match_ids = shots.Match_id.unique()

for match_id in match_ids:
    match_shots = shots[(shots['Match_id'] == match_id)]
    transform_coordinates_to_one_end(match_shots)

shots.to_csv('data/transformed_shots.csv', index=False)
