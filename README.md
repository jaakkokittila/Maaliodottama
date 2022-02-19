# Maaliodottama

Creating an expected goals prediction model with scikit-learn's K-nearest neighbor regression.
Data used for model creation parsed from Liiga's APIs.

## Project structure

### Data collection

```get_shots``` fetches and saves shot data to a csv file. <br/>
```get_matches``` gathers match and player data. Takes the season that you want to add to the data as an argument. <br/>
```transform_shots_to_one_end``` transforms the shot coordinates so that they are suitable for prediction. <br/>
```verify_transformation``` is used for checking that the transformation was succesful. <br/>
```fix_transformation``` removes the shots from data or fixes some that were transformed wrong. <br/>
```heatmap``` is used for visualizing the shot coordinates to finally check that they make sense. <br/>
```add_necessary_features``` adds the final features so that the model can work. <br/>

### Model creation

```train_model``` is used for training and saving the KNN model.

### Model use

```get_match_xgs``` gets match specific expected goals and saves them to a CSV file. <br/>
```get_player_xgs``` gets player speficic expected goals from season 2022 (for now) and saves them to a CSV file sorted highest to lowest.

### Others
```utilities``` contains functions that are used across multiple files.



