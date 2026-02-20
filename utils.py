import joblib
import numpy as np
import os

MODEL_PATH = "model/model.pkl"
SCALER_PATH = "model/scaler.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError("Model or scaler not found. Run train_model.py first.")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    return model, scaler


def predict_failure(input_data):
    model, scaler = load_model()

    input_scaled = scaler.transform([input_data])
    prediction = model.predict(input_scaled)

    return prediction[0]
