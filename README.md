# Project description
This repo was created as a capstone project for the Coding Bootcamp for Cybersecurity Professionals.</br>

**Goal**: Build a simple intrusion detection system (IDS) that can detect malicious network traffic using machine learning. 


# Features

-  The dataset described in `eda/data_desciption.md` was used to train a random forest model to differnciate between genuine and malicious network traffic. 
- On the basis of an exploratory data analysis (EDA) in the notebook `eda/eda.ipynb ` features were selected and transformed to improve model performance.
- Different baseline and random Forest models were created and evaluated in the notebook `model/model.ipynb`.
- Model performance can be further improved by hyperparameter tuning, the current best model was saved as `model/random_forest_model.pkl` and can be loaded to make predictions. 
- Make predictions based on the current best model running `predict.py ` (Functionality still has to be implemented)


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
- to be implemented
- Run the `predict.py` with ...

# Future improvements
- add the prediction functionality in `predict.py`
- clean the eda notebook and export the functions to the scripts folder for a better overview
- document model evaluation and comparison (model notebook)
- Train and compare different models for binary classification (e.g., XGboost)

# Disclaimer
This is a WIP, I am still learning (Oktober 2025)