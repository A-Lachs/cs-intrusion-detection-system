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

# ------------------------------------------ Variables ------------------------------

# there is no preprocessing for numerical features yet, so they are added here 
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
filename = "KDDTest+.txt"
# Models avaiable for prediction (saved as pkl files, or as functions when starting with BM)
MODELS = {
     "RF": 'model/random_forest_model.pkl',
     "BM_mal": baseline_model_malicious,
     "BM_rand": baseline_model_random,
     "BM_protocol": baseline_model_risky_protocol,
     } 

# path = "d:/PYTHON/CS_Bootcamp/programs/cs-intrusion-detection-system/data/KDDTest+.txt"
# ---------------------------------------------------------------------------------------

def run_prediction():
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
    file_path = arguments[2].strip()
    df_data= read_data_to_df(file_path) 
    
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
        # ------------------------------------------------------------
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

# ------------------------------------ main program -------------------------------------

if __name__ == "__main__":


    arguments = sys.argv # process CLI arguments


    # check nr of input arguments 
    if len(arguments) == 3:
        print('- Mode: prediction without evaluation.') #--> no y values given 
        predictions = run_prediction()

    elif len(arguments) == 4: # (optional)
        print('- Mode: prediction with evaluation') # X an y were given 
        predictions = run_prediction() 
        print('- Error: evaluation not implemented yet.')
        # TODO: preprocess target variable 
        # TODO: run evaluation func
                        
    else:
        print(f'--> Error: Wrong number of input arguments. Got {len(sys.argv)}, expected 3 or 4.')
            





    # CLI input: 
    # python predict.py RF test_input_X_20.txt
