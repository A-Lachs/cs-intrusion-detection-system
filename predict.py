import sys
import pandas as pd
import pickle

# add path to load own functions from .py files in scrips folder
project_path = "d:\\PYTHON\\CS_Bootcamp\\programs\\cs-intrusion-detection-system"
sys.path.insert(0, project_path + '\scripts')

from preprocessing import *

# ------------------------------------------ Variables ------------------------------

filename = "KDDTest+.txt"
MODELS = {"RF": 'model/random_forest_model.pkl'} # Models avaiable for prediction (saved as pkl files)
# path = "d:/PYTHON/CS_Bootcamp/programs/cs-intrusion-detection-system/data/KDDTest+.txt"


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
        print(f"- Chosen model: {arguments[1]}") 
        loaded_model = pickle.load(open(MODELS[arguments[1]], 'rb'))
    else:
        print(f"- Unknown model. Expects one of {MODELS.keys} as second argument.")

    
    # check input 2nd and 3rd arguments 
    if len(arguments) == 3:
        print('\n- Make prediction without evaluation.')
       
        # read 2nd argument as path to X data that includes y (for now )
        filepath = arguments[2]
        df_test = read_data_to_df(filepath)

        # ----------------------------------------------
        # data preprocessing / feature engineering
        # create a preprocessing wrapper function so we do not have to deal with the details here

        # ----------------------------------------------
        # make prediction
         #y_test_pred = loaded_model.predict(X_test)
         

    elif len(arguments) == 4: # (optional)
        print('\n- Make prediction with evaluation')
        # leave this as is for now 

    else:
        print(f' Wrong number of input arguments, got {len(sys.argv)}, expected 2 or 3.')