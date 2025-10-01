# Thyroid_Cancer_Prediction

This project uses a Random Forest model trained to predict the recurrence of thyroid cancer in patients. The application is powered by Streamlit, allowing users to input medical details and receive a probability score along with a recurrence prediction.

## Dataset Layout

The Dataset and Models are already in place, If you want to change the files you can replace these:

``` markdown
> dataset/
>    dataset.csv

> trained_model/
>    thyroid_recurrence_rf.pkl
>    thyroid_recurrence_rf_only.pkl
```

make sure that all the files are present in the root folder.

## Quickstart

1) Create and activate a virtual environment
>   ```python -m venv .venv```
source .venv/bin/activate  # Windows: .venv\Scripts\activate

> Run the file in the root folder
```bash
install_modules.bat
```
then follow the below steps to run the program

Quickstart



2) Ones again check if the `dataset` and `model` files are present in the root folder `dataset/` and `trained_model`

3) Now run the Application
   Open the `run.bat` file

OR

3) Target the location to the root folder, in any bash/powershell command
using `cd {location}`

Then type `streamlit run main.py` and the file will open in the web browse.
