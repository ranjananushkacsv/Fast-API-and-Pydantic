from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd
import numpy as np
from model.predict import predict_output, model, MODEL_VERSION
from schema.user_input import UserInput
    
app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Insurance Prediction API'}

#When we use services like aws(kubernetes) they require our api to have a health check point to ensure our api is running well
@app.get('/')
def health_check():
    return{
        'status':'Ok',
        'Version': MODEL_VERSION,
        'model_loaded': model is True
    }

@app.post('/predict')
async def predict_premium(data: UserInput):
    # Prepare input dataframe for the model
    user_input = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,  # FIXED: was data.income_lpa
        'occupation': data.occupation,
        'income_lpa': data.income_lpa
    }])
    
    try:
        prediction = predict_output(user_input)
    
    # Prepare response
        response = {
        "predicted_category": str(prediction)
    }
    
        return JSONResponse(
        status_code=200,
        content={"response": response}  # Match Streamlit's expected format
    )
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

@app.get('/')
async def root():
    return {"message": "Insurance Premium Prediction API is running"}