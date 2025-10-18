import sys
import pandas as pd
import pickle

# add path to load own functions from .py files in other dirs
project_path = "d:\\PYTHON\\CS_Bootcamp\\programs\\cs-intrusion-detection-system"
sys.path.insert(0, project_path + '\scripts')
sys.path.insert(0, project_path + '\model')

from preprocessing import *
from model_evaluation import *

# ------------------------------------------ Variables ------------------------------

output_file_name = 'prediction.txt'
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

    for key, value in models.items():
        if normalize_str(key) == normalize_str(input_arg):
            return key, value

    return


def write_prediction_output(output_file, predictions):
    # write predictions to a text file with one line per prediction
    with open(output_file, "w", encoding="utf-8", newline="") as f: 
            
            for prediction in predictions: 
                    f.write(str(prediction) + "\n")


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
    # read 3nd argument as path to X_test data 
    filepath = arguments[2]
    df_test = read_data_to_df(filepath) 
    # ------------------------------------------------------------
    
    if model[0].startswith('BM'):
        # Step 2: Load model
        # use baseline model function
        # ------------------------------------------------------------
        # Step 4: Prediction
        print("- Predicting ... ")
        y_prediction =  model[1](df_test)
        # ------------------------------------------------------------
    else:
        # Step 2: Load model
        # load model from pickle file 
        loaded_model = pickle.load(open(model[1], 'rb'))
        # ------------------------------------------------------------
        # step 3: Preprocessing / feature engineering
        print("- Data preprocessing ...")
        categorial_features = preprocessing_categories(df_test)
        # ------------------------------------------------------------
        # select features (must be the same the model was trained on)
        df_X = df_test[ numerical_features + categorial_features]
        # ------------------------------------------------------------
        # Step 4: Prediction 
        print("- Predicting ... ")
        y_prediction = loaded_model.predict(df_X)

    # ------------------------------------------------------------
    # Step 5: Write output file
    print(f"- Writing results to {output_file_name} ")
    write_prediction_output(output_file_name, y_prediction)
    # ------------------------------------------------------------
    
    return y_prediction

# ------------------------------------ main program -------------------------------------

if __name__ == "__main__":

    arguments = sys.argv # process CLI arguments

    # check if the 2nd argument is a model from the dict MODELS
    model = find_model(arguments[1], MODELS)

    if model:    
        print("\n--------------------")
        print(f"- Load model: {model[0]}") 

        # TODO: implement func to check inpurt arg 3 and 4 
       
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
            print(f'- Error: Wrong number of input arguments. Got {len(sys.argv)}, expected 3 or 4.')
            
    else:
        print(f"- Error: Unknown model. Expects one of {list(MODELS.keys())} as second argument.")




    # CLI input: 
    # python predict.py RF test_input_X_20.txt
