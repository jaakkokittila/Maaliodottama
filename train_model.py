import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import pickle
from sklearn import metrics

shots = pd.read_csv('data/shots_for_prediction.csv')

# I'll use seasons 2018, 2019, and 2020 for training, 2021 for testing and 2022 for validation.
# This is because the sample sizes are big enough that not randomizing shouldn't have that big of an effect.
# If I keep the two recent seasons away from model training I can get expected goals from this and the previous season.
# Stratification with the goals is also done this way conveniently, as otherwise there could be an uneven spread between different sets
# as there are only about 11000 goals in 172000 shots.

training_set = shots.iloc[0:113098]
testing_set = shots.iloc[113098:147062]
validation_set = shots.iloc[147062:len(shots)]

# I used AUC as the accuracy metric of the predictions as it was one that I am quite familiar with
# I originally thought to compare the amount of expected goals and actual goals in the training set,
# but that maybe gives too little emphasis on a single predictions accuracy and doesn't possibly
# notice if there is something fundamentally wrong with the model

def calculate_accuracy(pred_values, true_values):
    fpr, tpr, thresholds = metrics.roc_curve(true_values, pred_values)
    auc_score = metrics.auc(fpr, tpr)

    return auc_score

def fit_model(train_x, train_y, neighbors):
    knn = KNeighborsRegressor(n_neighbors=neighbors)
    knn.fit(train_x, train_y)

    return knn

def predict(model, test_x, test_y):
    predictions = model.predict(test_x)
    accuracy = calculate_accuracy(predictions, test_y)

    return accuracy

train_x = training_set[['Shot_x', 'Shot_y', 'Previous_shots', 'On_empty_net', 'Type_EvenStrengthShot', 'Type_PowerplayShot', 'Type_ShorthandedShot']]
train_y = training_set['Goal']

test_x = testing_set[['Shot_x', 'Shot_y', 'Previous_shots', 'On_empty_net', 'Type_EvenStrengthShot', 'Type_PowerplayShot', 'Type_ShorthandedShot']]
test_y = testing_set['Goal'].to_list()

validation_x = validation_set[['Shot_x', 'Shot_y', 'Previous_shots', 'On_empty_net', 'Type_EvenStrengthShot', 'Type_PowerplayShot', 'Type_ShorthandedShot']]
validation_y = validation_set['Goal'].to_list()


neighbors_to_test = (list(range(50, 501, 10)))

most_accurate_model_accuracy = 0
most_accurate_model = None

for neighbor in neighbors_to_test:
    model = fit_model(train_x, train_y, neighbor)
    accuracy = predict(model, test_x, test_y)

    if accuracy > most_accurate_model_accuracy:
        most_accurate_model = model
        most_accurate_model_accuracy = accuracy

    print('Neighbors: ', neighbor, ' ', accuracy)


# Save the most accurate model so it doesn't have to retrained every time
model_saver = open('knn_model', 'wb')
pickle.dump(most_accurate_model, model_saver)

# Finally test the accuracy on the validation set
validation_accuracy = predict(model, validation_x, validation_y)
print(validation_accuracy)

