import gradio as gr
import hopsworks
import joblib
import pandas as pd

# Log in to hopsworks, we have to make sure the API key is set
project = hopsworks.login()
fs = project.get_feature_store()

# Get the model from the model registry
mr = project.get_model_registry()
model = mr.get_model("wine_model", version=1)

# Download the model
model_dir = model.download()
model = joblib.load(model_dir + "/wine_model.pkl")
print("Model downloaded")


# Function that predicts the wine quality based on the input parameters
def wine(fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol, type):

    # Create a dataframe with the input parameters
    df = pd.DataFrame({
        'fixed_acidity': [fixed_acidity],
        'volatile_acidity': [volatile_acidity],
        'citric_acid': [citric_acid],
        'residual_sugar': [residual_sugar],
        'chlorides': [chlorides],
        'free_sulfur_dioxide': [free_sulfur_dioxide],
        'total_sulfur_dioxide': [total_sulfur_dioxide],
        'density': [density],
        'ph': [ph],
        'sulphates': [sulphates],
        'alcohol': [alcohol],
        'type': [type]
    })

    # Change the type to integer
    df['type'] = df['type'].map({'Red': 0, 'White': 1})

    # Predict the wine quality
    print(f"Predicting wine quality for: {df.to_dict()}, outcome is: {model.predict(df)[0]}")
    return round(model.predict(df)[0])
        
demo = gr.Interface(
    fn=wine,
    title="Wine Quality Predictive Analytics",
    description="Predict the quality of a wine based on its characteristics",
    allow_flagging="never",
    inputs=[
        gr.inputs.Slider(3.8, 15.9, 0.121, label= 'fixed_acidity'),
        gr.inputs.Slider(0.08, 1.58, 0.015, label= 'volatile_acidity'),
        gr.inputs.Slider(0.0, 1.66, 0.017, label= 'citric_acid'),
        gr.inputs.Slider(0.6, 65.8, 0.652, label= 'residual_sugar'),
        gr.inputs.Slider(0.009, 0.611, 0.006, label= 'chlorides'),
        gr.inputs.Slider(1.0, 289.0, 2.88, label= 'free_sulfur_dioxide'),
        gr.inputs.Slider(6.0, 440.0, 4.34, label= 'total_sulfur_dioxide'),
        gr.inputs.Slider(0.98711, 1.03898, 0.001, label= 'density'),
        gr.inputs.Slider(2.72, 4.01, 0.013, label= 'ph'),
        gr.inputs.Slider(0.22, 2.0, 0.018, label= 'sulphates'),
        gr.inputs.Slider(8.0, 14.9, 0.069, label= 'alcohol'),
        gr.inputs.Radio(["Red", "White"], label="Type"),
        ],
    outputs=[
        gr.outputs.Textbox(label="Quality"),
        ]
    )

demo.launch(debug=True)

