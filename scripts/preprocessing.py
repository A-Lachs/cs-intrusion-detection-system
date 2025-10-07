############################################################################
### collection of functions used for preprocessing & feature engineering ###
############################################################################

import pandas as pd
import numpy as np

VERBOSE = 0 # enable extra print statments with 1, disable with 0
BINARY_FEATURE_THRESHOLD = 0.99
BINARY_FEATURE_NEW_CAT = 1 # attention! add check: make sure the first cat is not also 1

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


def get_conditions(df_data: pd.Dataframe, feature: str, boundary:int):
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