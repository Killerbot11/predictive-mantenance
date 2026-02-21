import joblib
import pandas as pd
import os

def load_model():

    model = joblib.load("model/model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    columns = joblib.load("model/columns.pkl")

    return model, scaler, columns


def predict_failure(input_data):

    model, scaler, columns = load_model()

    # Convert input to DataFrame with correct order
    input_df = pd.DataFrame([input_data], columns=columns)

    # Scale while preserving column names
    input_scaled = pd.DataFrame(
        scaler.transform(input_df),
        columns=columns
    )

    prediction = model.predict(input_scaled)

    return prediction[0]
