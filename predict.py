import sys
import pandas as pd
import pickle

# add path to load own functions from .py files in scrips folder
project_path = "d:\\PYTHON\\CS_Bootcamp\\programs\\cs-intrusion-detection-system"
sys.path.insert(0, project_path + '\scripts')

from preprocessing import *

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
MODELS = {"RF": 'model/random_forest_model.pkl'} # Models avaiable for prediction (saved as pkl files)
# path = "d:/PYTHON/CS_Bootcamp/programs/cs-intrusion-detection-system/data/KDDTest+.txt"
# TODO: add baseline models for prediction 

# ----------------------------------------------
# demo code 
# goal: run predict.py with 3 arguments to make a precdiction for X
# where the arguments are the model, X-values an y-values (optional)
# when y_values are given: return evaluation metric
# when no y-values given: return prediction 

# ----------------------------------------------


if __name__ == "__main__":

    arguments = sys.argv # process arguments

    # check if the first argument is a model from the dict MODELS
    if arguments[1] in MODELS.keys():
        
        # load the model 
        print("\n----------")
        print(f"- Load model: {arguments[1]}") 
        loaded_model = pickle.load(open(MODELS[arguments[1]], 'rb'))
    else:
        print(f"- Unknown model. Expects one of {MODELS.keys} as second argument.")

    
    # check input 2nd and 3rd arguments 
    if len(arguments) == 3:
        #print('\n- Make prediction without evaluation.') --> no y values given 
        
        # TODO: provide seperate input for X and y values 
        # ----------------------------------------------
        # read 2nd argument as path to X data that includes y (for now )
        print("- Read data...")
        filepath = arguments[2]
        df_test = read_data_to_df(filepath) 
        # ----------------------------------------------
        # data preprocessing / feature engineering
        print("- Data preprocessing ...")
        categorial_features = preprocessing_categories(df_test)
        # ----------------------------------------------
        # select features (must be the same the model was trained on)
        df_X = df_test[ numerical_features + categorial_features]
        # ----------------------------------------------
        # make prediction 
        print("- Predicting... ")
        y_prediction = loaded_model.predict(df_X)
        print(y_prediction)
        # ----------------------------------------------
        # TODO: improve the output "prediciton"

    elif len(arguments) == 4: # (optional)
        print('\n- Make prediction with evaluation')
        # leave this as is for now 

    else:
        print(f' Wrong number of input arguments, got {len(sys.argv)}, expected 2 or 3.')