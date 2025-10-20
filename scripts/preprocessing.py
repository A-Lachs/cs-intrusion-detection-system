############################################################################
### collection of functions used for preprocessing & feature engineering ###
############################################################################

import pandas as pd
import numpy as np
import sys

project_path = "d:\\PYTHON\\CS_Bootcamp\\programs\\cs-intrusion-detection-system"
sys.path.insert(0, project_path + '\scripts')
# ---------------------------------------- variables ----------------------------------------

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
        # from EDA: assume 0 is the most frequent value and recode all other values to 1   
        data_df[new_feature] = (data_df[feature] != 0).astype(int) # fancy vectorized pd version (create bool mask and convert to int)
        # data_df[new_feature] = [x if x == 0 else 1 for x in data_df[feature]] # same 

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
        columns = [columns]  # convert co list
    
    for col in columns:
        df_data[col] = df_data[col].astype(to_type)

    return df_data


def is_categorical_dtype(data_df, feature):
    # returns true if col is categorical, otherwise false
    # because I cannot memorize this syntax
    return isinstance(data_df[feature].dtype, pd.CategoricalDtype) 
    

def recode_binary_target_feature(
    df_y: pd.DataFrame,
    input_feature: str,
    output_feature_name: str,
    normal_category_name: str = "normal"
) -> pd.DataFrame:
    """
    Recode a categorical variable (input_feature) into a binary categorical target variable (0/ 1), 
    where 0 stands for genuine and 1 for malicious network traffic. 
    The input feature must contain one category (normal_category_name) that identifies the 'genuine' class. 
    The normal_category_name (e.g., "normal") is mapped to 0, all other categories are mapped to 1.  

    Also accepts cases where the input feature is already binary (either as integers 0/1 or strings "0"/"1").
    In this case the normal_category_name is not used, only the conversion to int and category is done.

    Args:
        df_y (pd.DataFrame):        DF containing the input_feature column.
        input_feature (str):        Name of input feature to recode.
        output_feature_name (str):  Name of output feature to create.
        name_normal_category        Category representing the "normal" or "non-attack" class,
        (str, optional):            which will be mapped to 0. Defaults to "normal".
      
    Returns:
        pd.DataFrame:   With binary categorical target column added.
    """
    
    if input_feature not in df_y.columns:
        print(f"--> Error: No column named {input_feature}.")
        return None
    
    categories = list(df_y[input_feature].unique())

    # Case 1: input feature is binary numeric
    if set(categories).issubset({0, 1}):
        df_y[output_feature_name] = df_y[input_feature].astype("category")

    # Case 2: input feature is binary string
    elif set(categories).issubset({"0", "1"}):
        df_y[output_feature_name] = df_y[input_feature].astype(int).astype("category")
        
    # Case 3: input feature has category 'name_normal_category' mapped to 0
    elif normal_category_name in categories:
        # fancy vectorized version instead of list comprehension (create bool mask and convert to int)
        df_y[output_feature_name] = (df_y[input_feature] != normal_category_name).astype(int).astype("category")
        # df_y[output_feature_name] = [0 if x == name_normal_category else 1 for x in df_y[input_feature]]        
    else:
        print(f"--> Error: No category named {normal_category_name} in {categories}.")
        return None
    
    return df_y


def recode_to_binary_feature(data_df: pd.DataFrame, 
                             input_feature: str, 
                             output_feature_name: str,
                             verbose=VERBOSE, 
                             new_cat_name=BINARY_FEATURE_NEW_CAT,
                             threshold=BINARY_FEATURE_THRESHOLD):
    """
    Recode a numerical feature to binary categorical feature based on threshold.
    The input feature must have a value that occurs more frequently than the threshold 
    If true, all other feature values occur only rarely and are summarized into another category
    with the name new_cat_name (default 1). 
    
    - Note: This function assumes that the most frequent value is 0, and the default "other" category is 1.
            Returns None if the most freq value is not 0. 
    
    - Purpose: In the eda only the features that fullfill this criterion are selected for recoding.  

    Args:
        data_df (pd.DataFrame):     DF that contains the numerical input feature.
        input_feature (str):        Numerical feature to recode
        output_feature_name (str):  Name of the new feature column.
        verbose (0 or 1, optional): Allow additional print statements.
        new_cat_name (optional):    Name of the new category of the binary feature. 
                                    Defaults to 1. Assuming the other category is 0.
                                        Defaults to BINARY_FEATURE_NEW_CAT = 1
        threshold (float, optional):    Defaults to BINARY_FEATURE_THRESHOLD = 0.99.
    """
    
    feature_proportions = data_df[input_feature].value_counts(normalize=True).reset_index()
    most_frequent_value = feature_proportions.head(1)[input_feature].values[0] # first category
    
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
    
    # recode to most freq value vs all "other"
    # Here assume the most freq val is 0, all other will be 1 (new_cat_name)
    if most_frequent_value == 0:
        data_df[output_feature_name] = [x if x == most_frequent_value else new_cat_name for x in data_df[input_feature]]
    else:
        print(f"--> Attention: the most frequent value for '{input_feature}' is not 0 but {most_frequent_value}.\nCheck recoding categories.")
        return
    
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
        new_conditions:             DF mask with the new conditions. 
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
    Create a mask to recode a numerical freature of input DF df_data 
    to a categorical feature with 3 categories.
    -   Assumes 0 ist the most freq value and this is the first condition.
    -   Two further conditions are added (up to bondary and larger than boundary).

    Args:
        df_data (pd.Dataframe): DF that contrains the feature to recode.
        feature (str):       Numerical feature used to create the new conditions.
        boundary (int):      Boundary used to create condition 2 and 3.
    """
    
    new_conditions = [df_data[feature] == 0,
                      (df_data[feature] >= 1) & (df_data[feature] <= boundary),
                      df_data[feature] > boundary]
    return new_conditions

