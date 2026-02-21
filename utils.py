import joblib
import numpy as np
import os

MODEL_PATH = "model/model.pkl"
SCALER_PATH = "model/scaler.pkl"

def load_model():
    model_path = "model.pkl"
    scaler_path = "scaler.pkl"

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError("Model or scaler not found in repo.")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    return model, scaler


def predict_failure(input_data):
    model, scaler = load_model()

    input_scaled = scaler.transform([input_data])
    prediction = model.predict(input_scaled)

    return prediction[0]


