import os

import pandas as pd
import hopsworks
import joblib
import datetime
from PIL import Image
from datetime import datetime
import dataframe_image as dfi
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot
import seaborn as sns
import requests

# Log into Hopsworks
project = hopsworks.login()
fs = project.get_feature_store()

# Get the latest wine model
mr = project.get_model_registry()
model = mr.get_model("wine_model", version=1)
model_dir = model.download()
model = joblib.load(model_dir + "/wine_model.pkl")

# Get the feature view and a batch of data
feature_view = fs.get_feature_view(name="wine", version=1)
batch_data = feature_view.get_batch_data()

# Make a prediction on the batch data
y_pred = model.predict(batch_data)

# Get the last quality prediction of the batch
offset = 1
wine = y_pred[y_pred.size-offset]

# Create a string from the prediction
wine = str(round(wine))

# Save the prediction in a file
prediction_file = open("prediction.txt", "w")
prediction_file.write(wine)
prediction_file.close()

print("Wine quality predicted predicted: " + wine)

# Log into the project API
dataset_api = project.get_dataset_api()   

# Upload the prediction to the project
dataset_api.upload("./prediction.txt", "Resources/texts", overwrite=True)

# Get the feature group and read it into a dataframe
wine_fg = fs.get_feature_group(name="wine", version=1)
df = wine_fg.read() 

# Get the label of the last wine in the feature group
label = df.iloc[-offset]["quality"]

# Create a string from the label
label = str(round(label))

# Save the label in a file
label_file = open("label.txt", "w")
label_file.write(label)
label_file.close() 

print("Actual quality: " + label)
dataset_api.upload("./label.txt", "Resources/texts", overwrite=True)

# Create a feature group if it does not exist yet
monitor_fg = fs.get_or_create_feature_group(name="wine_predictions",
                                            version=1,
                                            primary_key=["datetime"],
                                            description="Wine quality Prediction/Outcome Monitoring"
                                            )

# Get the time now
now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
data = {
    'prediction': [wine],
    'label': [label],
    'datetime': [now],
    }

# Create a dataframe from the prediction and label
monitor_df = pd.DataFrame(data)
monitor_fg.insert(monitor_df, write_options={"wait_for_job" : False})

# Read all the predictions and labels from the feature group, and include the new one
history_df = monitor_fg.read()
history_df = pd.concat([history_df, monitor_df])

# Save the dataframe as an image and upload it to the project
df_recent = history_df.tail(20)
dfi.export(df_recent, './df_recent.png', table_conversion = 'matplotlib')
dataset_api.upload("./df_recent.png", "Resources/images/wine", overwrite=True)

# Create a confusion matrix
predictions = history_df[['prediction']]
labels = history_df[['label']]

# Print the unique quality predictions
print("Unique quality predictions: " + str(predictions.value_counts().count()))
for quality in predictions.value_counts().index:
    print(quality)

# Only create the confusion matrix when our wine_predictions feature group has examples of all qualities??
print("Number of different quality predictions to date: " + str(predictions.value_counts().count()))
if predictions.value_counts().count() == 7: #wine quality from 3 to 9 included
    results = confusion_matrix(labels, predictions)

    df_cm = pd.DataFrame(results, ['True quality 3', 'True quality 4', 'True quality 5', 'True quality 6', 'True quality 7', 'True quality 8', 'True quality 9'],
                            ['predicted quality 3', 'predicted quality 4', 'predicted quality 5', 'predicted quality 6', 'predicted quality 7', 'predicted quality 8', 'predicted quality 9'])

    cm = sns.heatmap(df_cm, annot=True)
    fig = cm.get_figure()
    fig.savefig("./confusion_matrix.png")
    dataset_api.upload("./confusion_matrix.png", "Resources/images/wine", overwrite=True)
else:
    print("You need 7 different quality predictions to create the confusion matrix.")
    print("Run the batch inference pipeline more times until you get 7 different wine quality predictions") 