# Thyroid_Cancer_Prediction

The Thyroid Cancer is a Random Forest Trained Prediction System, which helps in predicting the Reoccurrence of a past cancer patient, The goal is to train a model powered by Streamlit for the user to input the details and get the recurrence probability and whether they are likely or not to have cancer.

## Dataset Layout

The original dataset can be found in `dataset/dataset.csv` folder

If all the files are present:

> Run the `install_modules.bat` file
then follow the below steps to run the program

Quickstart

1) Create a venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

2) Ones again check if the `dataset` and `model` files are present in the root folder `dataset/` and `trained_model`

3) Now run the Application
   Open the `run.bat` file

OR

3) Target the location to the root folder, in any bash/powershell command
using `cd {location}`

Then type `streamlit run main.py` and the file will open in the web browse
