import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load your dataset
data = pd.read_csv("Crop_recommendation.csv")

X = data.drop("label", axis=1)
y = data["label"]

model = RandomForestClassifier()
model.fit(X, y)

# Save the trained model
pickle.dump(model, open("crop_recommendation_model.pkl", "wb"))

print("Model trained and saved!")
