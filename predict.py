import sys
import pandas as pd
import pickle


MODEL = "default_model"# basdeline models + models saved as pkl fils 

# ----------------------------------------------
# demo code 
# goal: run predict.py with 3 arguments to make a precdiction for X
# where the arguments are the model, X-values an y-values (optional)
# when y_values are given: return evaluation metric
# when no y-values given: return prediction 

# ----------------------------------------------
# process arguments
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv)) 

model = sys.argv[1]
X_test_path = sys.argv[2]
y_test_path = sys.argv[3] # optional 

# ----------------------------------------------
# load the model
loaded_model = pickle.load(open(model, 'rb'))
X_test = pd.read_csv(X_test_path)
y_test = pd.read_csv(y_test_path)


# ----------------------------------------------
# data preprocessing / feature engineering
# # select and convert features


# ----------------------------------------------
# make prediction
y_test_pred = loaded_model.predict(X_test)


# ----------------------------------------------
# make evaluation 