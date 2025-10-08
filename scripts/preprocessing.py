############################################################################
### collection of functions used for preprocessing & feature engineering ###
############################################################################

import pandas as pd
import numpy as np
import os

# ---------------------------------------- variables ----------------------------------------

file_name_train_data = "KDDTrain+.txt"
file_name_test_tata = "KDDTest+.txt"

VERBOSE = 0 # enable extra print statments with 1, disable with 0

# group features regarding their processing steps
TARGET_FEATURE = "attack_type " # recoded to binary feature (attack vs no attack) 
NUM_FEATURES = [
    'srv_serror_rate',
    'same_srv_rate',
    'dst_host_same_srv_rate',
    'dst_host_srv_diff_host_rate',
    'dst_host_count',
    'duration',
    'src_bytes',
    'dst_host_diff_srv_rate',
    'dst_host_srv_serror_rate',
    'dst_host_serror_rate',
    'srv_count',
    'dst_host_srv_rerror_rate',
    'dst_bytes',
    'dst_host_srv_count',
    'serror_rate',
    'diff_srv_rate',
    'dst_host_same_src_port_rate',
    'srv_diff_host_rate',
    'srv_rerror_rate',
    'dst_host_rerror_rate',
    'rerror_rate',
    'count']
CAT_FEATURES = [
    'logged_in', 
    'root_shell', 
    'is_guest_login', 
    'land', 
    'flag', 
    'difficulty_level', 
    'protocol_type', 
    'service']
RECODE_NUM_TO_BINARY_CAT = ['num_shells',
                    'urgent',
                    'num_root',           # --> works with threshold .99
                    'num_file_creations',
                    'num_failed_logins',
                    'su_attempted',
                    'num_access_files',
                    'wrong_fragment',     # --> works with threshold .99
                    ]
BINARY_FEATURE_THRESHOLD = 0.99     # only used to find categories in the training data
BINARY_FEATURE_NEW_CAT = 1          # attention! add check: make sure the first cat is not also 1
RECODE_NUM_TO_THREE_CAT = {
    'num_compromised': 10, 
    'hot': 5} 

# ------------------------------------ utility functions ------------------------------------

def preprocessing_categories(data_df):
    """
    Wrapper function that includes all preprocessing steps for the respective features. 

    - 1 step: convert categorical variables to categories 
        --> CAT_FEATURES
    - 2 step: recode numerical variables to binary categorical 
        --> RECODE_NUM_TO_BINARY_CAT
    - 3 step: recode numerical variables to categorical with 3 categories 
        --> RECODE_NUM_TO_THREE_CAT

    Returns list of all categorical features included in model training. 

    """
    new_categories = set([]) # all categorical features after preprocessing 

    # --- 1 step: convert categorical variables to categories
    for feature in CAT_FEATURES:
        data_df = convert_column_type(data_df, feature, 'category')
        
        # add feature to new categories 
        if is_categorical_dtype(data_df, feature):
            new_categories.add(feature)
        else:
            print(f"Feature {new_feature} not added to categories, check preprocessing.")

    # --- 2 step: recode numerical variables to binary categorical
    for feature in RECODE_NUM_TO_BINARY_CAT:
        new_feature = feature + "_cat"
        # note: do not use the threshold here, it was used in the training data to define the categories.
        # from EDA: assume 0 is the most frequent values and recode all other values to 1 
        data_df[new_feature] = [x if x == 0 else 1 for x in data_df[feature]]

        # convert to categorical 
        data_df = convert_column_type(data_df, new_feature, 'category')
        
        # add feature to new categories 
        if is_categorical_dtype(data_df, new_feature):
            new_categories.add(new_feature)
        else:
            print(f"Feature {new_feature} not added to categories, check preprocessing.")

    # --- 3 step: recode numerical variables to categorical with 3 categories
    category_labels = ["none", "low", "high"] 
    for feature, boundary in RECODE_NUM_TO_THREE_CAT.items():
        
        categories = get_conditions(data_df, feature, boundary)
        new_feature = feature + "_cat"
        recode_to_categories(data_df, new_feature, categories, category_labels)
        
        # add feature to new categories 
        if is_categorical_dtype(data_df, new_feature):
            new_categories.add(new_feature)
        else:
            print(f"Feature {new_feature} not added to categories, check preprocessing.")

    return list(new_categories)


def read_data_to_df(path_to_file:str) -> pd.DataFrame | None:
    """
    Read data from .txt or .csf file and return a pandas DF
    if the file can be found at 'path_to_file', otherwise return None.
    
    Data must have the same format as the data set the models were traiend on:
    "KDDTrain+.txt" (43 columns)

    Args:
        path_to_file (str): 

    Returns:
        pd.DataFrame | None: DF with column names as below. 
    """
    # TODO: catch exceptions

    column_names = ["duration", "protocol_type", "service","flag", "src_bytes", "dst_bytes", "land",
               "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised",
               "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", "num_access_files", 
               "num_outbound_cmds", "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
               "srv_serror_rate","rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", 
               "srv_diff_host_rate","dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", 
               "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
               "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
               "dst_host_srv_rerror_rate", "attack_type", "difficulty_level"]

    if not os.path.exists(path_to_file):
        print(f"Cannot find '{path_to_file}'")
        return []
    
    else:
        return pd.read_csv(path_to_file,  names=column_names)
    


def convert_column_type(df_data: pd.DataFrame, columns: list | str, to_type) -> pd.DataFrame:
    """ Convert data types of column(s) in a dataframe.

    Args:
        df_data (pd.DataFrame):     Input df
        columns (list | str):       Column name (str) or list of column names to convert. 
        to_type:                    Data type to convert in e.g. ('category', str, int).
    
    Returns:
        pd.DataFrame:               Input df with converted columns.
    """
    if isinstance(columns, str):
        # convert co list
        columns = [columns]
    for col in columns:
        df_data[col] = df_data[col].astype(to_type)

    return df_data


def is_categorical_dtype(data_df, feature):
    # returns true if col is categorical, otherwise false
    # because I cannot memorize this syntax
    return isinstance(data_df[feature].dtype, pd.CategoricalDtype) 
    

def recode_binary_target_feature(df_data: pd.DataFrame, input_feature: str, output_feature_name: str):

    # add a binary target variable (attack 1, no attack 0) to df_data, based on input feature 
    df_data[output_feature_name]= [0 if x == "normal" else 1 for x in df_data[input_feature]] 

    # convert to category
    df_data = convert_column_type(df_data, output_feature_name, 'category')
    return
     

def recode_to_binary_feature(data_df: pd.DataFrame, 
                             input_feature: str, 
                             output_feature_name: str,
                             verbose=VERBOSE, 
                             new_cat_name=BINARY_FEATURE_NEW_CAT,
                             threshold=BINARY_FEATURE_THRESHOLD):
    """
    Recode a numerical feature to binary categorical feature based on threshold.
    The input feature must have a value that occurs more frequently than the threshold.
    If true, all other feature values occur only rarely and are summarized into another category
    with the name new_cat_name (default 1). 

    Args:
        data_df (pd.DataFrame):     DF that contaisn the numerical input feature.
        input_feature (str):        Numerical feature to recode
        output_feature_name (str):  Name of the new feature column.
        verbose (0 or 1, optional): Allow additional print statements. Defaults to VERBOSE.
        new_cat_name (optional):    Name of the new category of the binary feature. 
                                    Here I used 1. A check needs to be added!
                                        Defaults to BINARY_FEATURE_NEW_CAT = 1
        threshold (float, optional):    Defaults to BINARY_FEATURE_THRESHOLD = 0.99.
    """
    
    feature_proportions = data_df[input_feature].value_counts(normalize=True).reset_index()
    most_frequent_value = feature_proportions.head(1)[input_feature].values[0] # name of the first category
    
    if threshold: # no threshold used for test data 
        # Sanity checks prior to recoding
        # the most frequent numerical value must occur more freq than threshold
        if feature_proportions.head(1).proportion.values[0] > threshold:
            if verbose:
                print(f"The most frequent value in {input_feature} is {most_frequent_value} with {feature_proportions.head(1).proportion.values[0]}%.")
                print(f"There are {len(feature_proportions)} different values in total.")
        else:
            print(f"The value {feature_proportions.head(1)[input_feature].values[0]} occurs {feature_proportions.head(1).proportion.values[0]}%.")
            print(f"No recoding done for {input_feature}, optionally change threshold for most frequent value: {threshold}.\n")
            return
    if verbose:
        print(f"Recoding {input_feature} to categories: {most_frequent_value} vs. {new_cat_name}.\n")
    
    # recode to most freq value vs all "other", here new_cat_name (1)
    # TODO: check that most_frequent_value is not 1 
    data_df[output_feature_name] = [x if x == most_frequent_value else new_cat_name for x in data_df[input_feature]]

    # convert to categorical 
    data_df = convert_column_type(data_df, output_feature_name, 'category') 
    return


def recode_to_categories(data_df: pd.DataFrame, 
                         new_feature_name:str, 
                         new_conditions, 
                         condition_labels:list, 
                         verbose=VERBOSE):
    """
    Recode a numerical feature to a categorical feature with the new conditions and labels as input.
    The new_conditions parameter is the mask that is created from the input feature 
    to define the categories of the new feature.
    The get_conditions() function can be used to create this mask.  

    Args:
        data_df (pd.DataFrame):     DF that contains the input feature.
        new_feature_name (str):     Name of the new feature column in the DF.
        new_conditions (_type_):    DF mask with the new conditions. 
        condition_labels (list):    List with the labels (str) of the new conditions-
        verbose (0 or 1, optional): Print statements. Defaults to VERBOSE.
    """
    
   
    # crate new column (feature)
    data_df[new_feature_name] = np.select(new_conditions, condition_labels, default="unknown")
    
    # check for unkown category and give warning
    if "unknown" in data_df[new_feature_name].unique():
        print("Warning: some values could not be assigned to the new categories, instead: 'unknown' ")
    else:
        # convert to category type
        data_df = convert_column_type(data_df, new_feature_name, 'category' )
        if verbose:
            print(f"Successfully recoded {new_feature_name}.\nNew categories: {list(data_df[new_feature_name].unique())}\n") 
    return  


def get_conditions(df_data: pd.DataFrame, feature: str, boundary:int):
    """
    Create a mask to recode a numerical freature of the DF 
    to a categorical feature with 3 categories.
    -   Assumes 0 ist the most freq value and this is the first condition.
    -   Two further conditions are added (up to bondary and larger than boundary).

    Args:
        df_data (pd.Dataframe): DF that contrains the feature
        feature (str):       Numerical feature used to create the new conditions.
        boundary (int):      Boundary used to create condition 2 and 3.

    Returns:
        _type_: _description_
    """
    
    new_conditions = [df_data[feature] == 0,
                      (df_data[feature] >= 1) & (df_data[feature] <= boundary),
                      df_data[feature] > boundary]
    return new_conditions