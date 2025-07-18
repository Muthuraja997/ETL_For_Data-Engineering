# app/app.py
import streamlit as st
import numpy as np
import pickle
import os

# Load model
MODEL_PATH = "../model/lung_cancer_model.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Lung Cancer Prediction", layout="centered")
st.title("🩺 Lung Cancer Prediction System")
st.write("Provide the details below to check the likelihood of lung cancer.")

# Input fields
age = st.slider("Age", 18, 100, 30)
gender = st.selectbox("Gender", ["Male", "Female"])
smoking = st.selectbox("Do you smoke?", ["Yes", "No"])
yellow_fingers = st.selectbox("Yellow fingers?", ["Yes", "No"])
anxiety = st.selectbox("Do you have anxiety?", ["Yes", "No"])
peer_pressure = st.selectbox("Under peer pressure?", ["Yes", "No"])
chronic_disease = st.selectbox("Chronic disease?", ["Yes", "No"])
fatigue = st.selectbox("Do you feel fatigue?", ["Yes", "No"])
allergy = st.selectbox("Do you have allergies?", ["Yes", "No"])
wheezing = st.selectbox("Do you experience wheezing?", ["Yes", "No"])
alcohol = st.selectbox("Consume alcohol?", ["Yes", "No"])
coughing = st.selectbox("Frequent coughing?", ["Yes", "No"])
shortness_breath = st.selectbox("Shortness of breath?", ["Yes", "No"])
swallowing_diff = st.selectbox("Swallowing difficulty?", ["Yes", "No"])
chest_pain = st.selectbox("Chest pain?", ["Yes", "No"])

# Preprocess inputs

def preprocess_inputs():
    return np.array([[
        1 if gender == "Male" else 0,
        age,
        1 if smoking == "Yes" else 0,
        1 if yellow_fingers == "Yes" else 0,
        1 if anxiety == "Yes" else 0,
        1 if peer_pressure == "Yes" else 0,
        1 if chronic_disease == "Yes" else 0,
        1 if fatigue == "Yes" else 0,
        1 if allergy == "Yes" else 0,
        1 if wheezing == "Yes" else 0,
        1 if alcohol == "Yes" else 0,
        1 if coughing == "Yes" else 0,
        1 if shortness_breath == "Yes" else 0,
        1 if swallowing_diff == "Yes" else 0,
        1 if chest_pain == "Yes" else 0,
    ]])


# Predict
if st.button("Predict"):
    input_data = preprocess_inputs()
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ High Risk of Lung Cancer")
    else:
        st.success("✅ Low Risk of Lung Cancer")
