from fastapi import FastAPI
import joblib
import pandas as pd
import os
from app.preprocessing import DateFeatureExtractor, FrequencyEncoder

import __main__
__main__.FrequencyEncoder = FrequencyEncoder
__main__.DateFeatureExtractor = DateFeatureExtractor

pipeline = joblib.load('app/model_ensemble.joblib')



app = FastAPI()

FRAUD_THRESHOLD = float(os.getenv("FRAUD_THRESHOLD", "0.75"))

@app.get('/')
def root():
    return {"message": 'Fraud Detection Model'}


@app.post('/predict')
def predict(data: dict):
    df_input = pd.DataFrame([data])
    prediction = pipeline.predict_proba(df_input)[0][1]
    is_fraud_result = bool(prediction > FRAUD_THRESHOLD)
    return {
        "is_fraud": is_fraud_result, 
        "fraud_probability": float(prediction),
        "threshold_used": FRAUD_THRESHOLD 
    }