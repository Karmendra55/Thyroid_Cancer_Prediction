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
```bash
python -m venv .venv
```
For Linux or Max:
```bash
source .venv/bin/activate
```
For Windows:
```bash
.venv\Scripts\activate
```

2) Now Run the file to install the dependencies
```bash
install_modules.bat
```

Run the Application
3a) Option A
```bash
run.bat
```

3b) Option B
- Open the command/bash and do the follow:
```bash
cd {Location of the "Drive:/file/.../Thyroid_Cancer_Prediction/"}
```
and type
```bash
streamlit run main.py
```

Make sure all files are placed as shown in the dataset layout, Once started, the application will open in your default web browser.

## Features

- Patient detail input via Streamlit form
- Prediction of thyroid cancer recurrence probability and voice narration
- The User can predict various different data and compare them with any of the saved ones.
