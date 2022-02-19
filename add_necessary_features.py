import pandas as pd

shots = pd.read_csv('data/transformed_shots.csv')

def z_score(column):
  return (column - column.mean()) / column.std()

goal = []
on_empty_net = []

# This feature is about how many shots there have been in the last 20 seconds, so for example if there have been many rebounds
# or some other situation where a goal is more likely because there are many shots coming
previous_shot_amounts = []

for i, row in shots.iterrows():
    previous_shots = shots[(shots['Id'] == row['Id']) &
                           (shots['Shooting_team'] == row['Shooting_team']) &
                           (shots['Time'] >= row['Time'] - 20) &
                           (shots['Time'] < row['Time'])]

    if row['Event_type'] == 'GOAL':
        goal.append(1)
    else:
        goal.append(0)

    if row['Blocker'] == 0:
        on_empty_net.append(1)
    else:
        on_empty_net.append(0)

    previous_shot_amounts.append(len(previous_shots))

shots['Goal'] = goal
shots['Previous_shots'] = previous_shot_amounts
shots['On_empty_net'] = on_empty_net

shots = pd.get_dummies(shots, columns=['Type'])

# These columns aren't useful in predicting goal probabilities
shots = shots.drop(columns=['Event_type', 'Left_team', 'Right_team', 'Period', 'Blocker', 'Time'])

# Standardize the coordinates so that they won't have a huge effect compared to other factors in predictions
# As well as previous shots as it would range more than any other column
shots[['Shot_x', 'Shot_y', 'Previous_shots']] = shots[['Shot_x', 'Shot_y', 'Previous_shots']].apply(lambda x: z_score(x))

shots.to_csv('data/shots_for_prediction.csv', index=False)