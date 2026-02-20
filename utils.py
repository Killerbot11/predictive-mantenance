import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_model():
    model_path = os.path.join(BASE_DIR, "model.pkl")
    scaler_path = os.path.join(BASE_DIR, "scaler.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError("model.pkl not found")

    if not os.path.exists(scaler_path):
        raise FileNotFoundError("scaler.pkl not found")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    return model, scaler
