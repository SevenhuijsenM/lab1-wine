import gradio as gr
from PIL import Image
import hopsworks

#login to hopswork
project = hopsworks.login()
fs = project.get_feature_store()

#get the dataset api
dataset_api = project.get_dataset_api()

#downloads form dataset the  predicted wine, the actual wine, the recent file and the confusion matrix
dataset_api.download("Resources/texts/prediction.txt", overwrite=True)
dataset_api.download("Resources/texts/label.txt", overwrite=True)
dataset_api.download("Resources/images/wine/df_recent.png", overwrite=True)
dataset_api.download("Resources/images/wine/confusion_matrix.png", overwrite=True)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Label("Today's Predicted quality")
            f = open("prediction.txt", "r")
            string = f.readline()
            f.close()
            input_img = gr.Textbox(string , elem_id="predicted-quality")
        
        with gr.Column():          
            gr.Label("Today's Actual quality")
            f = open("label.txt", "r")
            string = f.readline()
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
