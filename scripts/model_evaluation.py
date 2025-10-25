########################################################################
### collection of functions used for model classification evaluation ###
########################################################################

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# ------------------------------------- models ------------------------------------------

# define simple baseline models for model perfromance comparison 

def baseline_model_genuine(data):
    """ 
    Baseline model 1a. 
    Always predict 'genuine' = 0 network traffic.
    Don't worry. Be happy. 
    """
    return np.zeros(data.shape[0])

def baseline_model_malicious(data):
    """ 
    Baseline model 1b. 
    Always predict 'malicious' = 1 network traffic.
    Gotta catch them all. 
    """
    return np.ones(data.shape[0])

def baseline_model_random(data):
    """ 
    Baseline model 2.
    Randomly predict 'malicious' = 1 or 'genuine' = 0 network traffic. 
    """
    return [random.randint(0 ,1) for _ in range(data.shape[0])]

def baseline_model_risky_protocol(data):
    """ 
    Baseline model 3.
    When the protocol type is 'icmp' predict the network traffic is 'malicious' = 1.
    EDA revealed that over 80% of traffic with 'icmp protocol type was malicious.
    """
    return [1 if protocol == 'icmp' else 0 for protocol in data["protocol_type"]]

# ------------------------------------- prediction -------------------------------------


def make_predictions(model, Xtrain, Xtest):
    """
    Return predictions and probabilities for 1 class 
    from Xtrain and Xtest using a model object.
    """
    train_pred = model.predict(Xtrain)
    train_probs = model.predict_proba(Xtrain)[:, 1]

    test_pred = model.predict(Xtest)
    test_probs = model.predict_proba(Xtest)[:, 1]
    return train_pred, train_probs, test_pred, test_probs


# ------------------------------------- evaluation -------------------------------------


def print_classification_report(y_true, y_pred) -> dict:
    """
    Print and return a classification report (as dict).
    Note: in case one class is not predicted, prevent zero division warning
    by adding the parameter 'zero_division=0'. 
    """
    print("------"*10)
    cr = classification_report(y_true, y_pred, zero_division=0)
    print("Classification Report:\n", cr)
    print("------"*10)
    return classification_report(y_true, y_pred, output_dict=True, zero_division=0)


def add_metrics_to_dict(model_evaluation_dict:dict, 
                        model_name:str, 
                        dataset: str, 
                        y_true, 
                        y_pred, 
                        class_nr='1'):
    """
    Add dict of model_name -> dataset -> metrics to a dict 'model_evaluation_dict'.
    Print the classification report (cr) using helper func print_classification_report() 
    that returns cr as dict. 
    Usage: This function is used to collect the metrics of different models in one dict. 

    Args:
        model_evaluation_dict:  Dict to which a new dict is added.
        model_name (str):       Key of the Dict to be added
        dataset (str):          train or test
        y_true (list):          True class labels
        y_pred (list):          Predicted class labels
        class_nr (str):         Class the metrics refer to. Defaults to '1'.
                                Metrics are extracted from the classification report.

    Returns:
        dict:   data =  {'model_name': {
                            'train': {'accuracy': 0.99, 'precision': 0.99, 'recall': 0.99},
                            'test': {'accuracy': 0.91, 'precision': 0.91, 'recall': 0.91}}}
    """
   
    cr = print_classification_report(y_true, y_pred)
    metrics_keys = ['accuracy', 'precision', 'recall']
    metrics_values = [cr['accuracy'], cr[class_nr]['precision'], cr[class_nr]['recall']]
    metrics = dict(zip(metrics_keys, metrics_values))

    if model_name not in model_evaluation_dict:
        model_evaluation_dict[model_name] = {}   
        
    model_evaluation_dict[model_name][dataset] = metrics
    model_evaluation_dict
    return model_evaluation_dict


def dict_to_grouped_markdown_table(data:dict, floatfmt=".2f"):
    """
    Convert a nested dict of model_name -> dataset -> metrics
    into a Markdown table.
    Usage: From a 'model_evaluation_dict' print all the entries 
    in a format that can be copied into a markdown file to get 
    a pretty table for model comparison.

    data =  {'model_name': {
                'train': {'accuracy': 0.99, 'precision': 0.99, 'recall': 0.99},
                'test': {'accuracy': 0.91, 'precision': 0.91, 'recall': 0.91}}}
    """
    # get metric names 
    metrics = set()
    for model in data.values():             # iterate over models
        for dataset in model.values():      # iterate over train/test
            for metric in dataset.keys():   # iterate over metric names
                metrics.add(metric)
    metrics = sorted(metrics)
    
    # create table header
    headers = [h.title() for h in (["model", "dataset"] + metrics)]
    header_line = "| " + " | ".join(headers) + " |"
    align_line = "|:------|:--------|" + "|".join([":----------:" for _ in metrics]) + "|"
    lines = [header_line, align_line]
    
    # build rows of table
    for model, datasets in data.items():
        first = True
        for dataset, vals in datasets.items():
            row = []
            # only show model name in first row
            row.append(model if first else "")
            row.append(dataset)
            for metric in metrics:
                val = vals.get(metric, "")  # get value or empty str if missing
                # convert to str
                if isinstance(val, float):  # and format if float
                    row.append(format(val, floatfmt))
                else:
                    row.append(str(val))   
            lines.append("| " + " | ".join(row) + " |")
            first = False
    
    return "\n".join(lines)


def plot_confusion_matrix(y_true:list, y_pred:list, classes=None, normalize='true', verbose=1):
    """
    Plot a confusion matrix with group counts, normalized percentages, and class labels.

    Args:
        y_true (list):     True class labels
        y_pred (list):     Predicted class labels
        classes (list of str):      optional Names of classes in the order ["0", ""1" ...]
        normalize (str or None):    optional Normalization mode ('true', 'pred', 'all', or None)
        verbose (0 or 1):           if true print accuracy, precision and recall measures, 
                                    otherwise set to 0. 
    """

    # compute confusion matrix
    cf_matrix = confusion_matrix(y_true, y_pred)
    cf_matrix_norm = confusion_matrix(y_true, y_pred, normalize=normalize)

    # create labels (group names + count + percentage)
    group_names = ["TN", "FP", "FN", "TP" ] 
    group_counts = [f"{int(value)}" for value in cf_matrix.flatten()]
    group_percentages = [f"{value:.2%}" for value in cf_matrix_norm.flatten()]
    
    # combine into single label per cm cell
    labels = [f"{n}\n{c}\n{p}" for n, c, p in zip(group_names, group_counts, group_percentages)]
    labels = np.asarray(labels).reshape(2, 2) # need to have same shape as cf matrix

    # the actual plot
    plt.figure(figsize=(5, 4))
    ax = sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues', cbar=False)

    # add class labels if provided
    if classes is not None:
        tick_marks = np.arange(len(classes))
        ax.set_xticks(tick_marks + 0.5)  # center labels on cells
        ax.set_yticks(tick_marks + 0.5)
        ax.set_xticklabels(classes, rotation=45, ha='right', fontsize=12)
        ax.set_yticklabels(classes, rotation=0, fontsize=12)

    ax.set_xlabel("Predicted", fontsize=12)
    ax.set_ylabel("True", fontsize=12)
    ax.set_title("Confusion Matrix", fontsize=14)
    plt.tight_layout()
    plt.show()

    # print evaluation metrics accuracy, precision and recall
    if verbose:
        gc = [value for value in cf_matrix.flatten()] 
        print_evaluation_metrics(group_counts=gc)

    return 


def print_evaluation_metrics(group_counts: list):
    """
    Print accuracy, precision and recall.
    Requires an input a list with 4 integers as group counts from a confusion matrix,
    similar to group_names.
    Create a dict from group names and group counts and use it 
    to calculate the measures manually.
    
    This function is a memo for me, I know there are faster ways to get the metrics.  
    """
    group_names  = ["TN", "FP", "FN", "TP" ]

    # get the group_counts from confusion matrix and flatten to same format   
    # group_counts = [f"{int(value)}" for value in cf_matrix.flatten()]
    
    # dict to calculate metrics 
    v_dict = dict(zip(group_names,group_counts))
    
    # accuracy
    accuracy = (v_dict["TP"] + v_dict["TN"]) / (v_dict["TP"] + v_dict["FN"] + v_dict["TN"] + v_dict["FP"])
    print(f"Accuracy  {round(accuracy*100,2)}%  --> Proportion of all classifications (TN and TP) that were correct.")
    
    # precision
    if (v_dict["TP"] + v_dict["FP"]) == 0: # avoid nan when 0 division
        precision = 0.0   
    else:
        precision = v_dict["TP"] / (v_dict["TP"] + v_dict["FP"])
    print(f"Precision {round(precision*100,2)}%  --> Correctness: proportion of attack detections that were correct.")
    #  Precision = quality of positive predictions, (does not accout for correct detection of no attack - TN)!
    #  Precision improves when false positives decrease 
    #  HOW to improve Precision: INCREASE threshold for classification 
    #  --> less false pos but more false neg (bad for recall)
     
    # recall
    recall = v_dict["TP"]/(v_dict["TP"]+v_dict["FN"])
    print(f"Recall    {round(recall*100,2)}%  --> Sensitivity (TPR): proportion of actual attacks that could be correctly identified.")
    #  recall = models ability to detect attacks correctly (does not account for falase alarms!)
    #  recall = probabaility of detection
    #  Recall improves when false negatives decrease
    #  HOW to improve RECALL: DECREASE the threshold for classification -
    #  --> less false negatives, but more false positives (bad for precision)

    # precision-recall-tradeoff (you can only optimize for one, because improving one, makes the other worse)
    # depending on case decide for the measure to optimize! 
    
    # you can either be PRECISE and be CAREFUL that attact predictions are correct --> (High threshold)--> high risk of missing actual attacks (FN)
    # or you can make sure to be SENSITIVE and detect as much attacks as possible --> (LOW TRESHOLD) --> high risk of False Alarms (FP) 
    # FPR = proportion of actual negatives that were incorrecly classified as attacks 
    return 


def plot_feature_importances(model, df_X: pd.DataFrame, nr_features=10):
    """
    Plot the (nr_features) most important features from a tree based model. 

    Args:
        model (object):              Trained model. 
        df_X (pd.Dataframe):         DF with all the features the model was trained on.
        nr_features (int, optional): Number of most important features to plot. Defaults to 10.
    """
    # connect feature importances with feature names 
    feature_importances = model._final_estimator.feature_importances_
    dict_importances = {} # a dict to hold feature_name: feature_importance
    for feature, importance in zip(df_X.columns, feature_importances):
        dict_importances[feature] = importance # add the name/value pair 
    
    # convert dict to df
    df_importances = pd.DataFrame.from_dict(dict_importances, orient='index').rename(columns={0: 'Gini-importance'}).reset_index()
    df_importances = df_importances.sort_values(by='Gini-importance', ascending=False) # most important feature at top

    # plot feature importances 
    plt.figure(figsize=(6, 4))
    ax = sns.barplot(data=df_importances[:nr_features], 
                     x='Gini-importance', 
                     y='index', 
                     color='steelblue', 
                     orient='h')
    plt.ylabel('Feature importance')
    plt.yticks(size=10)
    plt.show()