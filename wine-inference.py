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

# Get the model registry
mr = project.get_model_registry()
model = mr.get_model("wine_model", version=1)
model_dir = model.download()
model = joblib.load(model_dir + "/wine_model.pkl")

# Get the feature store
feature_view = fs.get_feature_view(name="wine", version=1)
batch_data = feature_view.get_batch_data()

# Predict a single batch of data
y_pred = model.predict(batch_data)
offset = 1
last_wine = y_pred[y_pred.size - offset]

# Wine predicted
print("Wine predicted: " + last_wine)

# Save the value of the quality of the wine to a file
with open("./latest_wine_predicted.txt", "w") as f:
    f.write(last_wine)

# Upload the wine to Hopsworks
dataset_api = project.get_dataset_api()    
dataset_api.upload("./latest_wine_predicted.txt", "Resources/wines", overwrite=True)

# Get the actual wine
wine_fg = fs.get_feature_group(name="wine", version=1)
df = wine_fg.read() 

# Get the true label
label = df.iloc[-offset]["quality"]
print("Wine actual: " + label)

# Save the value of the quality of the wine to a file
with open("./latest_wine_actual.txt", "w") as f:
    f.write(label)

# Upload the wine to Hopsworks
dataset_api.upload("./latest_wine_actual.png", "Resources/wines", overwrite=True)

# Get the feature group of wine predictions
monitor_fg = fs.get_or_create_feature_group(name="wine_predictions",
                                            version=1,
                                            primary_key=["datetime"],
                                            description="Wine Prediction/Outcome Monitoring"
                                            )

# Create a datetime for the timestamp now
now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

# Create a dataframe with the prediction, label, and datetime
data = {
    'prediction': [last_wine],
    'label': [label],
    'datetime': [now],
    }
monitor_df = pd.DataFrame(data)

# Insert the dataframe into the feature group
monitor_fg.insert(monitor_df, write_options={"wait_for_job" : False})

# Get the history of predictions
history_df = monitor_fg.read()

# Add our prediction to the history, as the history_df won't have it - 
# the insertion was done asynchronously, so it will take ~1 min to land on App
history_df = pd.concat([history_df, monitor_df])

# Look at the last 4 predictions
df_recent = history_df.tail(4)
dfi.export(df_recent, './df_recent.png', table_conversion = 'matplotlib')
dataset_api.upload("./df_recent.png", "Resources/images", overwrite=True)

# Get the predictions nad labels
predictions = history_df[['prediction']]
labels = history_df[['label']]

# Only create the confusion matrix when our wine_predictions feature group has examples of all 7 wine qualities
print("Number of different wine predictions to date: " + str(predictions.value_counts().count()))
if predictions.value_counts().count() == 7:
    results = confusion_matrix(labels, predictions)

    df_cm = pd.DataFrame(results, ['True quality 3', 'True quality 4', 'True quality 5', 'True quality 6', 'True quality 7', 'True quality 8', 'True quality 9'],
                            ['Pred quality 3', 'Pred quality 4', 'Pred quality 5', 'Pred quality 6', 'Pred quality 7', 'Pred quality 8', 'Pred quality 9'])

    # Create a heatmap
    cm = sns.heatmap(df_cm, annot=True)
    fig = cm.get_figure()
    fig.savefig("./confusion_matrix.png")
    dataset_api.upload("./confusion_matrix.png", "Resources/images", overwrite=True)
else:
    print("You need 7 different wien quality predictions to create the confusion matrix.")
    print("Run the batch inference pipeline more times until you get 3 different wine quality") 