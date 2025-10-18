# Project description
This repo was created as a capstone project for the Coding Bootcamp for Cybersecurity Professionals.</br>

**Goal**: Build a simple intrusion detection system (IDS) that can detect malicious network traffic using machine learning. 


# Features

-  The dataset described in `eda/data_desciption.md` was used to train a random forest model to differenciate between genuine and malicious network traffic. 
- On the basis of an exploratory data analysis (EDA) in the notebook `eda/eda.ipynb ` features were selected and transformed to improve model performance.
- Different baseline models and random forest models were created and evaluated in the notebook `model/model.ipynb`.
- The random forest model performance can be further improved by hyperparameter tuning, the current best model was saved as `model/random_forest_model.pkl` and can be loaded to make predictions. 
- Make predictions about genuine or malicious network traffic by running `predict.py `(specifying model and input arguments as described below).


# How to run the program

## 1.  Set up the virtual environment

**Mac0S**
```
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

**WindowsOS git-bash CLI**
```
pyenv local 3.11.3
python -m venv .venv
source .venv/Scripts/activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

* Hint: use `--upgrade` to install packages listed in requirements.txt or update existing to pinned versions
* Add the '.env' file to the '.gitignore' file

## 2. Run the program 
- There are 2 different modes (theoretically - currently only mode 1 is implemented:)
    -   Mode 1: prediciton (required arguments --> model name, X-values)
    -   Mode 2: prediction and evaluation (required arguments --> model, X-values and corresponding y-values)
- Available models:
    - `'RF'` --> Trained random forest classifier model
    - `'BM_mal'` --> Baseline model, always predict malicious network traffic
    - `'BM_rand'` --> Baseline model, randomly predict genuine or malicius network traffic
    - `'BM_protocol'` --> Baseline model, predict malicious network traffic when imcp is used

- Input specifications:
    - The input has to have the same format as the on the model was trained on. 
    - The `test_input_X_20.txt` and `test_input_X_1.txt` are examples that were created from the test_data set from kaggle. 
    - Optionally, run `preprocessing.py` and specify the number of lines in the `create_test_input()` function to create larger input test files.

- Run the prediction from CLI with 'python predict.py model_name path_to_X_values'
    - where the model name is one of the available models mentioned above.
    - For example: `python predict.py RF test_input_X_20.txt`

- Result: This creates an output file 'prediction.txt.' where the prediction for each row in the input file is written in a new line: either 0 (genuine) or 1 (malicious) network traffic.


# Future improvements
- Add the Mode 2 functionality in `predict.py` (model evaluation, when true y-values are given)
- use kaggle API to get the data
- use seperate script to create test input
- eda: 
    - Document eda (summary)
    - Clean the eda notebook and export the functions to the scripts folder for a better overview
- models:
    - Document model evaluation and comparison (model notebook)
    - Clean the model notebook
    - Train and compare more models for binary classification (e.g., XGboost)

# Disclaimer
This is a WIP, I am still learning (October 2025)