from fastapi import FastAPI
import joblib
import pandas as pd

from app.preprocessing import DateFeatureExtractor, FrequencyEncoder

import __main__
__main__.FrequencyEncoder = FrequencyEncoder
__main__.DateFeatureExtractor = DateFeatureExtractor

pipeline = joblib.load('app/model_ensemble.joblib')



app = FastAPI()


@app.get('/')
def root():
    return {"message": 'Fraud Detection Model'}


@app.post('/predict')
def predict(data: dict):
    df_input = pd.DataFrame([data])
    prediction = pipeline.predict(df_input)
    
    return {"prediction": int(prediction[0])}