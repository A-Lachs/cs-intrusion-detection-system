
########################################################
### Create test input from the kaggle test data set  ### - seperate X and y data
########################################################

# run this from CLI: python create_test_input.py nr_cases
# where nr of cases defines the size of the subset 
# the maximum nr_cases = 22544

import sys
import os

from scripts.file_handling import *

# --------------------------------- variables ---------------------------------------------

# input data
TEST_DATA_FILE_PATH = "data\\" 
TEST_DATA_FILE_NAME = "KDDTest+.txt"

# output data
# creating subset (with seperate X and y files) from kaggle test data set
X_TEST_FILE_NAME = "test_input_X_" # nr_cases + .txt added in create_test_input() function
Y_TEST_FILE_NAME = "test_input_y_" # nr_cases + .txt added in create_test_input() function

# ------------------------------- functions  ----------------------------------------------


def create_test_input(input_file, nr_cases:int, output_X=X_TEST_FILE_NAME , output_y=Y_TEST_FILE_NAME):
    """
    Use the kaggle test data set to create a substet with length nr_cases. 
    To evaluate the prediction of a model this function automatically creates 
    seperate txt files for X and y values with the specified number of cases in the file name.

    Output files default: test_input_X_(nr_cases).txt, test_input_y_(nr_cases).txt
    """
    print("---------------"*2) 
    print("+++ Creating test data sets ...")

    # nr_cases must be int
    if not isinstance(nr_cases, int):
        try:
            nr_cases = int(nr_cases)      
        except(ValueError, TypeError):
            print(f"--> Error: {nr_cases} ist not an integer.")
            return

    # get test data set
    data_df = read_data_to_df(input_file)

    # exit when data could not be loaded correctly
    if data_df is None:
        print(f"--> Error: Terminating program.")
        print(f"[Debug] abs script path: {os.path.abspath(__file__)}")
        print(f"[Debug] cwd: {os.getcwd()}")
        return
    
    # nr_cases must not exceed length of test data set
    if nr_cases < len(data_df):
        
        # create subset test data set
        subset_df = data_df.sample(nr_cases)

        # seperate X and y data
        cols = [c for c in subset_df.columns if c != "attack_type"] # remove target "attack_type"
        df_X = subset_df[cols]
        df_y = subset_df["attack_type"]

        # create file names
        X_file_name=f"{output_X}{nr_cases}.txt"
        y_file_name=f"{output_y}{nr_cases}.txt"

        # write to txt file 
        df_X.to_csv(X_file_name, index=False, header=False, sep=",")
        df_y.to_csv(y_file_name, index=False, header=False, sep=",")

        print(f"--> Created files '{X_file_name}' and '{y_file_name}'.")
        return
    
    else:
        print(f"--> Error: The number of required cases {nr_cases} exceeds availability: {len(data_df)}.")
        return


# ------------------------------- run to create input   -----------------------------------------


if __name__ == "__main__":

    arguments = sys.argv

    if len(arguments) != 2:
        print(f"--> Error: Expected 2 CLI arguments, got {len(arguments)}")
    else:
        create_test_input(TEST_DATA_FILE_PATH + TEST_DATA_FILE_NAME, nr_cases=arguments[1])

