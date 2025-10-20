import sys
import pandas as pd
import pickle

# add path to load own functions from .py files in other dirs
project_path = "d:\\PYTHON\\CS_Bootcamp\\programs\\cs-intrusion-detection-system"
sys.path.insert(0, project_path + '\scripts')
sys.path.insert(0, project_path + '\model')

from preprocessing import *
from file_handling import *
from model_evaluation import *


# ------------------------------------------ variables ---------------------------------


# Note: there is no preprocessing for some numerical features, so they are added here for now
# atm only forest based (or baseline) models are available, where further preprocessing is not necessary
# based on eda results some numerical features are transformed to categories in the preprocessing step 

numerical_features = ['srv_serror_rate',
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

# Models avaiable for prediction (saved as pkl files, or as functions when starting with BM)
MODELS = {
     "RF": 'model/random_forest_model.pkl',
     "BM_mal": baseline_model_malicious,
     "BM_rand": baseline_model_random,
     "BM_protocol": baseline_model_risky_protocol,
     } 


# --------------------------------------- main functions -------------------------------


def run_prediction_process():
    """
    Wrapper function for the whole 5 step prediction process. 

    Step 1: Read data 
    Step 2: Load model
    Step 3: Preprocessing
    Step 4: Prediciton
    Step 5: Write output file
    
    Note: Steps 2 to 4 are different for baseline models 
    and models loaded from a pickle file. 
    """ 
    # ------------------------------------------------------------
    # Step 1: Read data
    # try to read 3rd CLI arg as path to data (X_test)
    file_path_X = arguments[2].strip()
    df_data = read_data_to_df(file_path_X) 
    
    if df_data is None:
        print("--> Terminating process: Data could not be loaded.")
        return
    # ------------------------------------------------------------
    # Step 2: Load model 
    # check if the 2nd argument is a model from the dict MODELS
    model = find_model(arguments[1], MODELS)
    
    if model is None:
        print("--> Terminating process: Model could not be loaded.")
        return

    # following steps differ, depending on model choice

    if model[0].startswith('BM'): 
        # use baseline model function
        # ------------------------------------------------------------
        # Step 4: Prediction
        print("---------------"*2) 
        print("+++ Predicting ...")
        y_prediction =  model[1](df_data)
        # ------------------------------------------------------------
    else: 
        # load model from pickle file 
        loaded_model = pickle.load(open(model[1], 'rb'))
        # ------------------------------------------------------------
        # step 3: Preprocessing / feature engineering
        print("---------------"*2)
        print("+++ Data preprocessing ...")
        categorial_features = preprocessing_categories(df_data)
        
        # select features (must be the same the model was trained on)
        df_preprocessed = df_data[ numerical_features + categorial_features]
        # ------------------------------------------------------------
        # Step 4: Prediction
        print("---------------"*2) 
        print("+++ Predicting ...")
        y_prediction = loaded_model.predict(df_preprocessed)

    # ------------------------------------------------------------
    # Step 5: Write to output file
    print("---------------"*2)
    # output file name is defined in scripts/file_handling.py
    write_prediction_output(y_prediction)
    # ------------------------------------------------------------
    
    return y_prediction


def run_evaluation_process():
    """
    Wrapper function for the 3 step evaluation process. 

    Step 1: Read y data 
    Step 2: Preprocessing
    Step 3: Evaluation
    """ 
    # ------------------------------------------------------------
    # 1. Step: read 4th CLI arg as path to y_true data
    file_path_y = arguments[3].strip()
    df_y = read_single_column_data(file_path_y)
    
    if df_y is None:
        print("--> Terminating process: Evaluation data could not be loaded.")
        return
    # ------------------------------------------------------------
    # step 2. preprocess y data
    print("---------------"*2)
    print("+++ Data preprocessing ...")
    # TODO: control edge cases 
    df_target = recode_binary_target_feature(df_y, "attack_type", "target")

    if len(df_y) != len(y_prediction):
        print("--> Error: length of X and y values do not match!")
        print("--> Terminating evaluation process.")
        return
    # ------------------------------------------------------------
    # Step 3: evaluation
    print("---------------"*2) 
    print("+++ Evaluating predictions ...")
    evaluation_report = print_classification_report(df_target["target"], y_prediction)
    # TODO: add short report with relevant metrics 
    return evaluation_report


# ------------------------------------ main program -------------------------------------------


if __name__ == "__main__":

    arguments = sys.argv 
    # process CLI arguments
    # # arguments[1] --> model specification
    # # arguments[2] --> path to X values for which you want to make a prediciton
    # # arguments[3] --> path to y values which are the true values matching your X values

    # Proceed with processing depening on nr of CLI arguments
    if len(arguments) == 3 or len(arguments) == 4:
        
        # Mode 1: Prediction - for 3 and 4 arguments 
        y_prediction = run_prediction_process()

        # Mode 2: Evaluation - for 4 arguments
        # proceed when predictions were successfully made 
        # and y data (true values) are given
        if y_prediction is not None and len(arguments) == 4:
            evaluation = run_evaluation_process()
            #print(evaluation)

    else:
        print(f'--> Error: Wrong number of input arguments. Got {len(sys.argv)}, expected 3 or 4.')
            