import pandas as pd

shots = pd.read_csv('data/transformed_shots.csv')

def flip_match_to_other_end(match_id):
    match_shots = shots[shots['Match_id'] == int(match_id)]
    for i, row in match_shots.iterrows():
        new_x = -1 * (row['Shot_x'] - 1030)
        shots.loc[i, 'Shot_x'] = new_x
        new_y = -1 * (row['Shot_y'] - 515)
        shots.loc[i, 'Shot_y'] = new_y

# Something has gone with transforming these matches, so I'll just drop them since there aren't that many
matches_to_drop = ['2192018', '222019', '232019', '3492020']

# This match has just been transformed to the wrong end, so I'll just flip these coordinates the other way
matches_to_flip = ['1192019', '6232021']

for match in matches_to_drop:
    match_indexes = shots[shots['Match_id'] == int(match)].index
    shots = shots.drop(index=match_indexes)

for match in matches_to_flip:
    flip_match_to_other_end(match)

shots.to_csv('data/transformed_shots.csv', index=False)

