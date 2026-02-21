import joblib
import pandas as pd

def load_model():
    model = joblib.load("model/model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    columns = joblib.load("model/columns.pkl")
    return model, scaler, columns


def predict_failure(input_data):
    model, scaler, columns = load_model()

    input_df = pd.DataFrame([input_data], columns=columns)
    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)

    return prediction[0]