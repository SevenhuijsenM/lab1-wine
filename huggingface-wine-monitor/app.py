import gradio as gr
from PIL import Image
import hopsworks

#login to hopswork
project = hopsworks.login()
fs = project.get_feature_store()

#get the dataset api
dataset_api = project.get_dataset_api()

#downloads form dataset the  predicted wine, the actual wine, the recent file and the confusion matrix
dataset_api.download("Resources/wines/latest_wine_predicted.txt")
dataset_api.download("Resources/wines/latest_wine_actual.txt")
dataset_api.download("Resources/images/df_recent.png")
dataset_api.download("Resources/images/confusion_matrix.png")

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Label("Today's Predicted quality")
            f = open("latest_wine_predicted.txt", "r")
            string = print(f.readline())
            f.close()
            input_img = gr.Textbox(string , elem_id="predicted-quality")
        
        with gr.Column():          
            gr.Label("Today's Actual quality")
            f = open("latest_wine_actual.txt", "r")
            string = print(f.readline())
            f.close()
            input_img = gr.Textbox(string, elem_id="actual-quality")        
    
    with gr.Row():
        
        with gr.Column():
            gr.Label("Recent Prediction History")
            input_img = gr.Image("df_recent.png", elem_id="recent-predictions")
        with gr.Column():          
            gr.Label("Confusion Maxtrix with Historical Prediction Performance")
            input_img = gr.Image("confusion_matrix.png", elem_id="confusion-matrix")        

demo.launch()
