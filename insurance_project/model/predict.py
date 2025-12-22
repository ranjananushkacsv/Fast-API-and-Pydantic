import pickle
import pandas as pd
import numpy as np

# Import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    
MODEL_VERSION = '1.0.0'

def predict_output(user_input: dict):
    input_df = pd.DataFrame([user_input])
    
    # Make prediction
    output = model.predict(input_df)[0]
    
    return output