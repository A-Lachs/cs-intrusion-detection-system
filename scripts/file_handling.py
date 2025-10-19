### python script to collect functionality for input and output file handling

import pandas as pd
import os

# --------------------------------- variables ---------------------------------------------

# input 
file_name_train_data = "KDDTrain+.txt"
file_name_test_data = "KDDTest+.txt"

# output 
output_file_path = "" #'data/' 
output_file_name = 'prediction.txt'
OUTPUT_FILE = output_file_path + output_file_name


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


def read_data_to_df(path_to_file:str) -> pd.DataFrame | None:
    """
    Read data from .txt or .csv file and return a pandas DF
    if the file can be found at 'path_to_file', otherwise return None.
    
    Data must have the same format as the data set the models were traiend on:
    "KDDTrain+.txt" (43 columns or 42 columns without target column.)

    Args:
        path_to_file (str): 

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
        print(f"--> Error: Cannot find path: '{path_to_file}'.")
        return 
    
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
        return

    return pd.read_csv(path_to_file,  names=column_names)


# ------------------------------- create test input  -----------------------------------------

def create_test_input(input_file, output_X:str, output_y:str, nr_lines:int) :
    """
    To test the prediction create seperate input files for X_test and y_test. 
    Choose nr of lines from the test data. 
    """
    
    data_df = read_data_to_df(input_file)
    cols = [c for c in data_df.columns if c != "attack_type"] # remove target "attack_type"
    df_X = data_df[cols]
    df_y = data_df["attack_type"]

    if nr_lines < len(data_df):
    
        df_X.head(nr_lines).to_csv(f"../{output_X}_{nr_lines}.txt", index=False, header=False, sep=",")
        df_y.head(nr_lines).to_csv(f"../{output_y}_{nr_lines}.txt", index=False, header=False, sep=",")
        print(f"Created files '{output_X}_{nr_lines}' and '{output_y}_{nr_lines}'.")
        return
    else:
        print(f"Number of input lines {nr_lines} exceeds available lines {len(data_df)}.")
        return





# ------------------------------- output file  -----------------------------------------


def write_prediction_output(predictions, output_file=OUTPUT_FILE):
    # write predictions to a text file with one line per prediction
    print(f"+++ Writing predictions to: '{os.path.abspath(output_file)}'")
    with open(output_file, "w", encoding="utf-8", newline="") as f: 
            
            for prediction in predictions: 
                    f.write(str(prediction) + "\n")


    # TODO: think about more user friendly solution for output file path 
    # problem: I have a data folder in gitignore, but you would have to manually create it or change the path
    # iterim solution: save file in cwd
    # idea: ask for user input, advantage: could also offer alternative ouput options 
    # idea: add a flag 

# ------------------------------- run to creete input   -----------------------------------------

if __name__ == "__main__":

# create some test input 
    create_test_input("..\\data\\" + file_name_test_data, 'test_input_X', 'test_input_y',1)