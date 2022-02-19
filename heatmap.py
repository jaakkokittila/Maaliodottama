import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import LinearSegmentedColormap

# Create a heatmap of shots and goals to make sure that my coordinate transformation was succesful

shots = pd.read_csv('data/transformed_shots.csv')
x = shots['Shot_x'].to_list()
y = shots['Shot_y'].to_list()

goals = shots[shots['Event_type'] == 'GOAL']
goals_x = goals['Shot_x']
goals_y = goals['Shot_y']

rink = plt.imread('Rink.png')

# This color map I just copied straight from Stack Overflow

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white", "blue","violet","red"])

red_high = ((0., 0., 0.),
         (.3, .5, 0.5),
         (1., 1., 1.))

blue_middle = ((0., .2, .2),
         (.3, .5, .5),
         (.8, .2, .2),
         (1., .1, .1))

green_none = ((0,0,0),(1,0,0))

cdict3 = {'red':  red_high,

     'green': green_none,

     'blue': blue_middle,

     'alpha': ((0.0, 0.0, 0.0),
               (0.3, 0.5, 0.5),
               (1.0, 1.0, 1.0))
    }

dropout_high = LinearSegmentedColormap('Dropout', cdict3)

plt.xlim(0, 1030)
plt.ylim(0, 515)
plt.hexbin(x, y, cmap=dropout_high, gridsize=(60, 30))
plt.colorbar()
plt.imshow(rink, aspect='equal', extent=(0,1030,0,515))
plt.show()

plt.xlim(0, 1030)
plt.ylim(0, 515)
plt.hexbin(goals_x, goals_y, cmap=dropout_high, gridsize=(60, 30))
plt.colorbar()
plt.imshow(rink, aspect='equal', extent=(0,1030,0,515))
plt.show()