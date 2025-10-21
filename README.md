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

## 2. Download the data set from kaggle

- You need to download the data from kaggle:
    - If you want to create and train your own models or run the notebooks for eda and modeling 
    - If you want to create your own test input files from the kaggle dataset
    - see: `eda/data_description.md` 

- You do not need to download the data set:
    - When you want run predictions and evaluations with the provided models and test_input.txt files
    - Or provide your own input (in the same format)

## 3.  Select parameters and input 

There are 2 different modes (triggered by the amount of CLI arguments).
-   **Mode 1: Prediciton** 
    -   Required CLI arguments: 
        -   model name
        -   X-values (path to txt or csv file)
    -   Output: 
        - file 'prediction.txt' with a prediction (0 or 1) for each line of X-values

-   **Mode 2: Prediction and evaluation**
    -   Required CLI arguments: 
        -   model name 
        -   X-values (path to txt or csv file)
        -   corresponding y-values (path to txt or csv file)
    -   Output: 
        -   file 'prediction.txt' with a prediction (0 or 1) for each line of X-values
        -   evaluation: prints full classification report (for now)  

- Available models:
    - `'RF'` --> Trained Random Forest Classifier
    - `'BM_mal'` --> Baseline Model, always predict malicious network traffic (1)
    - `'BM_rand'` --> Baseline Model, randomly predict genuine or malicius network traffic 
    - `'BM_protocol'` --> Baseline model, predict malicious network traffic when imcp is used

- Input specifications:
    - ` X-values`
        -   This input has to have the same format as the model was trained on (same number and names of features). 
        -   The files `test_input_X_20.txt` (20 lines) and `test_input_X_1.txt`(one line) contain example cases that were created from the test_data set from kaggle (one case per line). 
        -   These can be used to test predictions about genuine or malicious network traffic.  
        
    - `y-values`
        - This input is required when you know the true classification of the cases for which a prediction is made and you want to evaluate the model performance. 
        - The number of X-values and y-values has to match, e.g. use `test_input_X_20.txt` with `test_input_y_20.txt`.    

- Create own test input files (optional),
    - requires download of kaggle data set
    - Create larger test input files from the kaggle test data set with the `create_test_input.py` script
    - run `create_test_input.py nr_cases` where `nr_cases` is and integer that specifies the number of lines in the  
    - Note: The maximum nr of cases is 22544.

## 4. Run the program from CLI  
-   with `python predict.py model_name path_to_X_values path_to_y_values`

    -   where the `model_name` is one of `RF`, `BM_mal`, `BM_rand` or `BM_protocol`
    -   and the `path_to_X_values` and `path_to_y_values` can be specified as the test files provided `test_input_X_20.txt` and `test_input_y_20.txt`

- **Example for Mode 1: prediction** 
    -    predict whether network traffic of one example case is genuine or malicious with the random baseline model
    - `python predict.py BM_rand test_input_X_1.txt`

- **Example for mode 2: prediction and evaluation** 
    -   redict whether network traffic of 20 example casesis genuine or malicious  with the Random Forest Classifier
    -   `python predict.py RF test_input_X_1.txt test_input_y_1.txt`

## 5. Interpret the results

- Each prediction procress creates an output file `prediction.txt` where the prediction for each case (line) in the input file is written in a new line: either 0  for genuine or 1 for malicious network traffic.
- For model evaluation a classification report is printed, compare accuracy, precision and recall values


# Future improvements
- improve evaluation output and description 
- improve automation: use kaggle API to get the data
- eda: 
    - Create eda summary (md file)
    - Clean the eda notebook and export the functions to the scripts folder for a better overview
- models:
    - Create summary for model evaluation and comparison (md file)
    - Clean the model notebook
    - add own precrocessing func to pipeline
    - Train and compare more models for binary classification (e.g., XGBoost)

----
----
Disclaimer: 
This is a WIP, I am still learning
(repo started october 2025)