# lab1-wine

This is the assignment for Wine prediction for Alessandro Meroli and Merlijn Sevenhuijsen

The repository includes both the iris and the wine data that is required for a succesful lab. 
Within /iris/ all the iris data is put whereas the main directory contains all the wine prediction data.

On a test set (and training that is) an accuracy of 55% was obtained, which means that there is still room for a better preprocessing. Our guess is that it is due to some classes (quality == 3) being underrepresented in the data. For future work more preprocessing should be done to make the proportion of qualities even.

Here are the links to huggingface repositories:

Wine monitoring: https://huggingface.co/spaces/dussen/wine_monitor
Wine prediction: https://huggingface.co/spaces/dussen/wine_prediction

Iris monitoring: https://huggingface.co/spaces/dussen/iris
Iris prediction: https://huggingface.co/spaces/dussen/IrisPrediction

Everything is a gradio application for the GUI.
