import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

print("Loading dataset...")

# NASA FD001 column names
cols = ['unit','time','op1','op2','op3'] + [f's{i}' for i in range(1,22)]

# -------- ROBUST DATA LOADING --------
data = pd.read_csv(
    "data/train_FD001.txt",
    sep=r"\s+",
    header=None,
    engine="python"
)

# Drop empty columns caused by trailing spaces
data = data.dropna(axis=1, how='all')

# NASA FD001 should have 26 columns
data = data.iloc[:, :26]

# Assign column names
data.columns = cols

print("Dataset loaded successfully")
print("Shape:", data.shape)

# -------- RUL CALCULATION --------
rul = data.groupby('unit')['time'].max().reset_index()
rul.columns = ['unit','max_time']
data = data.merge(rul, on='unit')
data['RUL'] = data['max_time'] - data['time']

# Convert to failure classification
data['Failure'] = data['RUL'].apply(lambda x: 1 if x <= 30 else 0)

# Drop unnecessary columns
data = data.drop(['max_time','RUL','unit','time'], axis=1)

print("Preprocessing done")

# -------- FEATURES & LABEL --------
X = data.drop('Failure', axis=1)
y = data['Failure']

# -------- SCALING --------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------- TRAIN TEST SPLIT --------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print("Training model...")

# Faster training for demo
model = RandomForestClassifier(n_estimators=20, random_state=42)
model.fit(X_train, y_train)

# -------- SAVE MODEL --------
os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("Model Trained & Saved Successfully")
