#######################################################################
### collection of functions used for input and output file handling ###
#######################################################################

import pandas as pd
import os
from pathlib import Path
import json


# --------------------------------- variables ---------------------------------------------
VERBOSE=0

# input: kaggle data set names
file_name_train_data = "KDDTrain+.txt"
file_name_test_data = "KDDTest+.txt"

# json file that maps features to preprocessign steps 
features_json_filename = "eda/features_for_processing.json" 

# prediction output 
output_file_path = "" #'data/' 
output_file_name = 'prediction.txt'
OUTPUT_FILE = output_file_path + output_file_name

# TODO: think about more user friendly solution for prediction output file path 
# problem: I have a data folder in gitignore, but you would have to manually create it or change path
# iterim solution: save file in cwd
# idea: ask for user input, advantage: could also offer alternative ouput options 
# idea: add a flag 
# idea: use kaggle api


# -------------------------------  helper functions ---------------------------------------


def get_project_root(criterions=("README.md","pyproject.toml", ".git")) -> Path | None:
    """
    Helper function. Return the project root directory by walking upward from this file's location, 
    looking for criterions (that define a project root dir). 
    Args:
        criterions (tuple[str]): filenames that identify the project root
    Returns:
        Path: Path object pointing to the project root directory.
              If no criterion matches, returns None.
    """
    # 1. Get absolute path of directory of this script
    start_dir = Path(__file__).resolve().parent  #  __file__ --> returns location of this file
    all_parent_dirs = list(start_dir.parents)    # seqeuence of all parent dirs
    
    # 2. Iterate through this directory and all its parents
    for parent in [start_dir] + all_parent_dirs:
        # Check whether any of the criterion files exist in the current parent
        for criterion in criterions:   
            full_path =  os.path.join(parent, criterion)
            if os.path.exists(full_path):
                # print(f"Returning root dir: {parent}"")
                return parent
            
    # If nothign found all the way up, return None
    print("--> Error: Could not find root dir.")
    return None


def load_features_for_preprocessing(json_file_name=features_json_filename, verbose=VERBOSE):
    
    #print("\n--- Loading features from json")
    project_root = get_project_root()
    if project_root:
        # create path to file
        file_path = os.path.join(project_root, json_file_name) 
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                features_for_processing = json.load(f)
        except Exception as e:
             print(f"An error occurred: {e}")
             return
        else:        
            if verbose: 
                print("--- Loaded featuresfrom json file:")
                for processing_step, features in features_for_processing.items():
                    print(f"For {processing_step} got {len(features)} features.")

            return features_for_processing
    print("--> Error: No features loaded.")    
    return 

# ------------------------------- process CLI arguments -----------------------------------


def normalize_str(s:str)-> str:
     return s.strip().lower()


def find_model(input_arg:str, models:dict) -> tuple | None:
    """
    If the input_arg is a key in the dict models 
    return its key and value, otherwise None. 

    - input_arg and dict key are normalized with the helper function normalize_str()

    Args:
        input_arg (str): model name
        models (dict):   where the keys are the model names and values the models

    Returns:
        tuple | None:   key and value of the model dict or None
    """
    print("---------------"*2) 
    print("+++ Loading model ...")

    for key, value in models.items():
        if normalize_str(key) == normalize_str(input_arg):
            print(f"--> Chosen model: {key}")
            return key, value
    print(f"--> Error: Unknown model '{input_arg}'. Expects one of {list(models.keys())} as 2nd argument.")
    return


def path_ok(file_path: str) -> bool:
    """
    Check whether the given file path exists.
    Args:
        file_path (str): Path to a file.
    Returns:
        bool: True if file exists, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"--> Error: Cannot find path: '{file_path}'.")
        return False
    return True


def read_data_to_df(path_to_file:str) -> pd.DataFrame | None:
    """
    Read data from .txt or .csv file and return a pandas DF
    if the file can be found at 'path_to_file', otherwise return None.
    
    Data must have the same format as the data set the models were traiend on:
    "KDDTrain+.txt" (43 columns or 42 columns without target column.)

    Args:
        path_to_file (str): path to txt or csv file

    Returns:
        pd.DataFrame | None: DF with column names as below. 
    """

    col_names_full = ["duration", "protocol_type", "service","flag", "src_bytes", "dst_bytes", "land",
               "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised",
               "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", "num_access_files", 
               "num_outbound_cmds", "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
               "srv_serror_rate","rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", 
               "srv_diff_host_rate","dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", 
               "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
               "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
               "dst_host_srv_rerror_rate", "attack_type", "difficulty_level"]
    
    print("---------------"*2) 
    print("+++ Reading data ...")

    # Check path
    # print(f"[DEBUG] Checking path: {os.path.abspath(path_to_file)}")
    # print(f"[DEBUG] Exists? {os.path.exists(path_to_file)}")

    if not os.path.exists(path_to_file):
        print(f"--> Error: Cannot find file here: '{path_to_file}'.")
        return None

    # count the nr of columns from txt file
    with open(path_to_file, 'r') as f:
        first_line = f.readline().strip()

    num_cols = len(first_line.split(","))

    # depending on the number of columns, adapt column_names
    if num_cols == 43:
        column_names = col_names_full
    elif num_cols ==42:
        column_names = [c for c in col_names_full if c != "attack_type"] # remove target
    else:
        print(f"--> Error: Unexpected number of columns: {num_cols}, has to be 43 or 42.")
        return None
    
    df_X = pd.read_csv(path_to_file,  names=column_names)
    print(f"--> Loaded {len(df_X)} values from '{path_to_file}'.")

    return df_X
    

def read_single_column_data(path_to_file: str) -> pd.DataFrame | None:
    """
    Reads a text or csv file expecting 1 column (1 str per line).
    Usage: import y-values (taget variable or true classificatons).
    Accepts:
      - Case 1: column format (1 str per line)
      - Case 2: single line format (with strings seperated by comma, semicolor or space)
    
    Returns:
        pd.DataFrame with one column, or None if something goes wrong.
    """
    print("---------------"*2) 
    print("+++ Reading y data ...")

    if not os.path.exists(path_to_file):
        print(f"--> Error: Cannot find file: '{path_to_file}'.")
        return None

    with open(path_to_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print(f"--> Error: File '{path_to_file}' is empty.")
        return None

    # Case 1: column format  (1 str per line)
    if len(lines) > 1:
        data = lines
    else:
        # Case 2: single line format (split it by del)
        line = lines[0]
        if "," in line:
            data = line.split(",")
        elif ";" in line:
            data = line.split(";")
        elif " " in line:
            data = line.split()
        else:
            data = [line]  # just 1 element

    # Remove empty str and spaces
    data = [item.strip() for item in data if item.strip()]

    df = pd.DataFrame(data, columns=["attack_type"])
    print(f"--> Loaded {len(df)} values from '{path_to_file}'.")

    return df


# ------------------------------- output file  -----------------------------------------------


def write_prediction_output(predictions: list, output_file=OUTPUT_FILE):
    """
    Creates a text file with one line per prediction (0 or 1). 

    Args:
        predictions (list):     List with predictions.
        output_file (str, opt): Path and file name.  
                                Defaults to OUTPUT_FILE='prediction.txt'.
    """
    print(f"+++ Writing predictions to: '{os.path.abspath(output_file)}'")
    with open(output_file, "w", encoding="utf-8", newline="") as f: 
            
            for prediction in predictions: 
                    f.write(str(prediction) + "\n")