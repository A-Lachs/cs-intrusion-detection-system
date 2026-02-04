# Intrusion Detection System using Machine Learning

This repository contains my capstone project for the Coding Bootcamp for Cybersecurity Professionals (October - Novermber, 2025).</br>
The goal of the project is to demonstrate practical understanding of python, data analysis and machine learning fundamentals, applied to a cybersecurity use case.

**Project Goal**: 
Build a simple intrusion detection system (IDS) that classifies network traffic as genuine or malicious using supervised machine learning.

# Dataset 

-   **NSL-KDD99** with seperate datasets for model training and testing
-   Datasets were downloaded from **kaggle**, a description and overview of the data can be found [here](eda/data_description.md).

-   Feature `attack type` was used to create a **target variable** for **binary classification**:
    -   `0` --> genuine network traffic
    -   `1` --> malicious network traffic 

    ![Image: pie plot of attack types](images/pie_plot_attack_types.png)


# Approach & Methodology

## Exploratory Data Analysis (EDA)

- Performed extensive EDA to understand feature distributions and relationships
- Selected and transformed features based on EDA insights to improve model performance
- EDA work is documented in the [eda](eda/eda.ipynb) notebook

## Modeling & Evaluation

### Evaluation Metrics

Models were evaluated on both training and unseen test data using **Accuracy**, **Precision**, and **Recall**. 
-   Accuracy provides a general performance overview
-   Recall was emphasized over precision due to the intrusion detection context, where missing malicious traffic is typically more costly than false alarms

### Baseline Models

Several baseline models were implemented:
- Always predict a single class
- Random prediction
- A simple protocol-based heuristic derived from EDA

These models performed at or near chance level (~50% accuracy) on unseen data, providing a meaningful benchmark for evaluating more complex approaches.

### Random Forest Classifier

The primary model used was a Random Forest classifier, selected for its ability to handle heterogeneous feature types and capture non-linear relationships in network traffic data. 

- Multiple Random Forest variants were trained and evaluated to assess model capacity and generalization behavior.

- The best-performing model was saved as: `model/random_forest_model.pkl` and can be loaded directly to make predictions on new data   

## Results & Key Insights

Baseline vs. Random Forest Performance (Test Data)


| Model	| Accuracy	| Precision	| Recall|
| --- | ----------- |---|---|
|Baseline (best)	|~0.50	|high	|very low|
|Random Forest (basic)	|0.81	|0.91	|0.74|
|Random Forest (tuned)	|0.84	|0.92	|0.80|

- Baseline models performed at or near chance level (~50% accuracy), highlighting the need for more complex models.

- Random Forest models significantly outperformed baselines and generalized reasonably well to unseen data.
- The basic Random Forest showed signs of overfitting, performing much better on training than test data.
- Hyperparameter tuning improved generalization and recall, which is critical for IDS applications.

- The best-performing model achieved an accuracy of 84%, precision of 92%, and recall of 80% on the test set, clearly outperforming all baseline models. 

- Even the best model still misses some attacks, highlighting opportunities for further improvement.




# Features

-  The kaggle [dataset](eda/data_description.md) NSL-KDD99 was used to train a random forest model to distinguish genuine from malicious network traffic (binary classification). 
- On the basis of an exploratory data analysis (EDA) features were selected and transformed to improve model performance in the [eda](eda/eda.ipynb) notebook.
- Different baseline models and random forest models were created and evaluated in the [model](model/model.ipynb) notebook. A summary and disusssion can be found [here](model/model_summary.md).  
- The random forest model performance can be further improved by hyperparameter tuning, the current best model was saved as `model/random_forest_model.pkl` and can be loaded to make predictions. 
- Make predictions about genuine or malicious network traffic by running `predict.py` (specifying model and input arguments as described below).

---
- Train and evaluate multiple models for intrusion detection
- Compare baseline models against a Random Forest classifier
- Run predictions via a command-line interface
- Optionally evaluate predictions using known labels
- Modular structure to support experimentation and future extensions

# How to run the program

## 1.  Set up the virtual environment

### Mac0S/Linux
```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (Git Bash)
```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/Scripts/activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

* Hint when pip installing requirements: 
    -   use `--upgrade` flag carefully
    -   optionally try a dry run: `pip install --upgrade --upgrade-strategy only-if-needed --dry-run -r requirements.txt`
    -   when there are no conflicts, use: `pip install --upgrade --upgrade-strategy only-if-needed -r requirements.txt`


## 2. Add `.gitignore` file

To avoid committing environment variables or datasets:
- Add `.env` and `data/` to your .gitignore
- works for Git Bash and macOS/Linux

```bash
{
  echo ""
  echo "# Environment and data files"
  grep -qxF '.env' .gitignore || echo '.env'
  grep -qxF 'data/' .gitignore || echo 'data/'
} >> .gitignore
```


## 3. Download the data set

Download the NSL-KDD99 dataset from [kaggle](https://www.kaggle.com/datasets/kaggleprollc/nsl-kdd99-dataset/data) and save in in the `data/` directory.

- You **need the dataset** if you want to:
    - Train models from scratch
    - Run the notebooks for [eda](eda/eda.iypnb) and [modeling](model/model.ipynb) 
    - Generate custom test input files from the kaggle data (described below)
        - Create own test input files (optional):
        - requires download of kaggle data set
        - Create larger test input files from the kaggle test data set with the `create_test_input.py` script
        - run `create_test_input.py nr_cases` where `nr_cases` is and integer that specifies the number of lines in the  
        - Note: The maximum nr of cases is 22544.
  
- You **do not need the dataset** if you want to:
    - Run predictions using the provided models
    - Use the included test input files
    - Or provide your own input (in the same format as the test input)
    

## 4.  Run predictions

Predictions are made using `predict.py`, which supports two modes depending on the number of CLI arguments.

### Mode 1: Prediciton only 
**Required arguments**
-   model name
-   X-values file (txt or csv)

**Output**
- `'prediction.txt'` containing one prediction per input row

### Mode 2: Prediction and evaluation
**Required arguments**
-   model name 
-   X-values file 
-   corresponding y-values file

**Output**
-    `'prediction.txt'`
-   printed  classification report 

---
### Available models
- `'RF'` --> Random Forest Classifier (best)
- `'BM_mal'` --> Baseline, always predicting malicious
- `'BM_rand'` --> Baseline, random prediction
 - `'BM_protocol'` --> Baseline, predict malicious when protocol is 'imcp' 
---

### Input Specifications
` X-values`
- Must match feature format used for training
- Example files created from test data set:
    - `test_input_X_1.txt` ( 1 input case)
    - `test_input_X_20.txt` (20 input cases)  
        
`y-values`
- Required only for evaluation 
- Number of labels must match the numer of X-values 

## 5. Example commands 

### Prediction only
Predict whether network traffic of one example case is genuine or malicious with the random baseline model.

```bash
python predict.py BM_rand test_input_X_1.txt
```


### Prediction and evaluation
Predict whether network traffic of 20 example cases is genuine or malicious with the Random Forest Classifier and print a classification report.

```bash
python predict.py RF test_input_X_20.txt test_input_y_20.txt
```

## 6. Interpreting results

- Predictions are written to `prediction.txt`
    - `0` → genuine traffic
    - `1` → malicious traffic
- When model evaluation is enabled, a classification report is printed to compare accuracy, precision, and recall (discussed [here](model/model_summary.md)).


# Future improvements

-   Improve evaluation output and reporting
-   Automate dataset retrieval using the Kaggle API
-   Refactor EDA code into reusable scripts
-   Extend preprocessing steps within the modeling pipeline
-   Train and compare additional models (e.g. XGBoost)