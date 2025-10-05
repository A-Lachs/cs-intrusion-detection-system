############################################################################
### collection of functions used for preprocessing & feature engineering ###
############################################################################

import pandas as pd
import numpy as np

VERBOSE = 0 # enable extra print statments with 1, disable with 0
BINARY_FEATURE_THRESHOLD = 0.99

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
                             new_cat_name='other',
                             threshold=BINARY_FEATURE_THRESHOLD):
    
    # recode a numerical feature to binary categorical feature based on threshold 

    feature_proportions = data_df[input_feature].value_counts(normalize=True).reset_index()
    most_frequent_value = feature_proportions.head(1)[input_feature].values[0]
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
    data_df[output_feature_name] = [x if x == most_frequent_value else new_cat_name for x in data_df[input_feature]]

# convert to categorical 
    data_df = convert_column_type(data_df, output_feature_name, 'category') 
    return


def recode_to_categories(data_df: pd.DataFrame, new_feature_name, new_conditions, condition_labels, verbose=VERBOSE):
    # recode a feature with the new conditions and condition labels as input 
    
    # crate new column 
    data_df[new_feature_name] = np.select(new_conditions, condition_labels, default="unknown")
    
    # check for unkown category and give warning
    if "unknown" in data_df.num_compromised.unique():
        print("Warning: some values could not be assigned to the new categories, instead: 'unknown' ")
    else:
        # convert to category type
        data_df = convert_column_type(data_df, new_feature_name, 'category' )
        if verbose:
            print(f"Successfully recoded {new_feature_name}.\nNew categories: {list(data_df[new_feature_name].unique())}\n") 
    return  


def get_conditions(df_data, feature, boundary):
    # vassumes 0 ist the most freq value = 1 condition
    new_conditions = [df_data[feature] == 0,
                      (df_data[feature] >= 1) & (df_data[feature] <= boundary),
                      df_data[feature] > boundary]
    return new_conditions