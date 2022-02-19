import pandas as pd
import matplotlib.pyplot as plt

shots = pd.read_csv('data/transformed_shots.csv')

match_ids = shots.Id.unique()


# All shots have transformed so that they are shot at the left end of the rink
# The middle line of the rink is at about x 500 so if there are many shots
# Shot after 500 it might suggest that there is something gone wrong in the transformation of that match
# So I'll view the scatter plot of these matches and make further decisions based on that and the actual shotmap on the Liiga website

for match_id in match_ids:
    match_shots = shots[shots['Id'] == match_id]
    shots_from_right_end = match_shots[match_shots['Shot_x'] > 500]

    if len(shots_from_right_end.index) > 10:
        print(match_id)
        x = match_shots['Shot_x']
        y = match_shots['Shot_y']

        plt.scatter(x, y)
        plt.show()
