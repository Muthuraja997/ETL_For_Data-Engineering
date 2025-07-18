# scripts/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

# Load dataset
data = pd.read_csv("../data/lung_cancer_data.csv")

# Features and label
X = data.drop('LUNG_CANCER', axis=1)
y = data['LUNG_CANCER']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
os.makedirs("../model", exist_ok=True)
with open("../model/lung_cancer_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully!")
