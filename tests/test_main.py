from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app 

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": 'Fraud Detection Model'}

def test_prediction_endpoint():
    data = {
        "trans_date_trans_time": "2019-04-27 03:36:32",
        "cc_num": 676245600876,
        "merchant": "fraud_Hudson-Ratke",
        "category": "grocery_pos",
        "amt": 292.07,
        "first": "Ashley",
        "last": "Blanchard",
        "gender": "F",
        "street": "292 Lowe Dam Suite 858",
        "city": "West Palm Beach",
        "state": "FL",
        "zip": 33417,
        "lat": 26.7197,
        "long": -80.1248,
        "city_pop": 459921,
        "job": "Historic buildings inspector/conservation officer",
        "dob": "1960-06-14",
        "trans_num": "d808b5c3d739a88b7d4ad8a9b5f25d5e",
        "unix_time": 1335497792,
        "merch_lat": 27.285337,
        "merch_long": -81.114135
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    
    data = response.json()
    assert "is_fraud" in data
    assert "fraud_probability" in data
    assert isinstance(data["is_fraud"], bool)