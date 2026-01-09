from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class DateFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = pd.DataFrame(X).copy()
        X_copy['trans_date_trans_time'] = pd.to_datetime(X_copy['trans_date_trans_time'])
        X_copy['dob'] = pd.to_datetime(X_copy['dob'])

        hours = X_copy['trans_date_trans_time'].dt.hour
        is_night = ((hours >= 22) | (hours < 4)).astype(int)

        weekday = X_copy['trans_date_trans_time'].dt.weekday
        
        age = (X_copy['trans_date_trans_time'] - X_copy['dob']).dt.days // 365

        return pd.DataFrame({
            'is_night': is_night,
            'weekday': weekday,
            'age': age
        })
    
class FrequencyEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.freq_maps = {}

    def fit(self, X, y=None):
        for col in X.columns:
            self.freq_maps[col] = X[col].value_counts(normalize=True).to_dict()
        return self

    def transform(self, X):
        X_copy = X.copy()
        for col in X_copy.columns:
            X_copy[col] = X_copy[col].map(self.freq_maps[col]).fillna(0)
        return X_copy