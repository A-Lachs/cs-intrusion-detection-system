import sys
import pandas as pd
import pickle

# add path to load own functions from .py files in scrips folder
project_path = "d:\\PYTHON\\CS_Bootcamp\\programs\\cs-intrusion-detection-system"
sys.path.insert(0, project_path + '\scripts')

from preprocessing import *

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
MODELS = {"RF": 'model/random_forest_model.pkl'} # Models avaiable for prediction (saved as pkl files)
# path = "d:/PYTHON/CS_Bootcamp/programs/cs-intrusion-detection-system/data/KDDTest+.txt"
# TODO: add baseline models for prediction 

# ----------------------------------------------
# demo code 
# goal: run predict.py with 3 arguments to make a precdiction for X
# where the arguments are the model, X-values an y-values (optional)
# when y_values are given: return evaluation metric
# when no y-values given: return prediction 

# ---------------------------------------------------------------------------------------

def write_prediction_output(output_file, predictions):
    # write predictions to a text file with one line per prediction
    with open(output_file, "w", encoding="utf-8", newline="") as f: 
            
            for prediction in predictions: 
                    f.write(str(prediction) + "\n")

def run_prediction():
     
    # ------------------------------------------------------------
    # read 3nd argument as path to X_test data 
    filepath = arguments[2]
    df_test = read_data_to_df(filepath) 
    # ------------------------------------------------------------
    # data preprocessing / feature engineering
    print("- Data preprocessing ...")
    categorial_features = preprocessing_categories(df_test)
    # ------------------------------------------------------------
    # select features (must be the same the model was trained on)
    df_X = df_test[ numerical_features + categorial_features]
    # ------------------------------------------------------------
    # make prediction 
    print("- Predicting ... ")
    y_prediction = loaded_model.predict(df_X)
    # ------------------------------------------------------------
    # write prediction output file
    print(f"- Writing results to {output_file_name} ")
    write_prediction_output(output_file_name, y_prediction)
    # ------------------------------------------------------------
    
    return y_prediction

# ------------------------------------ main program -------------------------------------

if __name__ == "__main__":

    arguments = sys.argv # process CLI arguments

    # check if the first argument is a model from the dict MODELS
    if arguments[1] in MODELS.keys():
        
        # load the model 
        print("\n--------------------")
        print(f"- Load model: {arguments[1]}") 
        loaded_model = pickle.load(open(MODELS[arguments[1]], 'rb'))

        # check input nr of input arguments 
        if len(arguments) == 3:
            print('- Mode: prediction without evaluation.') #--> no y values given 
            predictions = run_prediction()

        elif len(arguments) == 4: # (optional)
            print('- Mode: prediction with evaluation') # X an y were given 
            predictions = run_prediction() 

            # TODO: preprocess target variable 

        else:
            print(f' Wrong number of input arguments, got {len(sys.argv)}, expected 3 or 4.')

    else:
        print(f"- Unknown model. Expects one of {MODELS.keys} as second argument.")

    # CLI input: 
    # python predict.py RF test_input_X_20.txt
