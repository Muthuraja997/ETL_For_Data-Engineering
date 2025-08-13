from flask import Flask, render_template, request, jsonify
import sklearn
import pickle
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import wikipedia
import datetime

# Load env vars
load_dotenv()

app = Flask(__name__)

# Load your trained crop recommendation model
model = pickle.load(open("crop_recommendation_model.pkl", "rb"))

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_gemini = genai.GenerativeModel("models/gemini-1.5-flash")

# --- Gemini prompt helpers ---

def gemini_generate(prompt):
    try:
        response = model_gemini.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini API error: {e}"

# 1. Crop details (main info)
def get_crop_details(crop_name):
    prompt = f"""
Provide comprehensive agricultural information about the crop '{crop_name}' in numbered sections:

1. General Description
2. Ideal Soil Type and Conditions
3. Sowing Method and Season
4. Recommended Fertilizers and Application
5. Common Pests and Precautions
6. Harvesting Period and Techniques
7. Average Yield
8. Uses and Benefits
9. Disadvantages or Challenges

Provide clear, practical info useful to farmers.
"""
    return gemini_generate(prompt)

# 2. Crop Image from Wikipedia
def get_crop_image(crop_name):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{crop_name}"
        res = requests.get(url).json()
        return res.get("thumbnail", {}).get("source", "")
    except:
        return ""

# 3. Week-by-Week Farming Calendar
def get_farming_calendar(crop_name):
    prompt = f"""
Create a detailed week-by-week farming calendar for the crop '{crop_name}'. 
List activities to perform each week from sowing to harvest in clear numbered points.
"""
    return gemini_generate(prompt)

# 4. Possible Diseases based on current conditions
def get_possible_diseases(crop_name, temperature, humidity, rainfall):
    prompt = f"""
Based on the crop '{crop_name}', temperature {temperature}°C, humidity {humidity}%, and rainfall {rainfall} mm, 
list the most common diseases and pests the crop might face, with brief descriptions.
"""
    return gemini_generate(prompt)

# 5. Custom Fertilizer Mix
def get_fertilizer_mix(crop_name, N, P, K, ph):
    prompt = f"""
For the crop '{crop_name}', given soil nutrients Nitrogen: {N}, Phosphorus: {P}, Potassium: {K}, and pH level: {ph}, 
recommend a custom fertilizer mix including types, quantities, and application tips.
"""
    return gemini_generate(prompt)

# 6. Market Price for Tamil Nadu (Static example, extendable)
def get_market_price(crop_name):
    # Static dummy data, you can replace with real API later
    price_dict = {
        "rice": "₹32/kg",
        "wheat": "₹25/kg",
        "cotton": "₹50/kg",
        "maize": "₹20/kg",
        "groundnut": "₹45/kg",
        "sugarcane": "₹28/kg"
    }
    return price_dict.get(crop_name.lower(), "Price data not available")

# 7. AI FAQ — Gemini chatbot style
def get_gemini_faq_response(crop_name, question):
    prompt = f"""
You are an expert agricultural assistant. Answer the question below concisely and clearly.

Crop: {crop_name}
Question: {question}
Answer:
"""
    return gemini_generate(prompt)

# Routes

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    try:
        # Extract inputs
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        features = [N, P, K, temperature, humidity, ph, rainfall]

        # Predict crop
        prediction = model.predict([features])[0]

        # Fetch all dynamic data
        crop_image_url = get_crop_image(prediction)
        crop_info = get_crop_details(prediction)
        farming_calendar = get_farming_calendar(prediction)
        diseases = get_possible_diseases(prediction, temperature, humidity, rainfall)
        fertilizer_mix = get_fertilizer_mix(prediction, N, P, K, ph)
        market_price = get_market_price(prediction)

        # Render results page with all data
        return render_template("result.html",
                               crop=prediction,
                               image_url=crop_image_url,
                               crop_info=crop_info,
                               farming_calendar=farming_calendar,
                               diseases=diseases,
                               fertilizer_mix=fertilizer_mix,
                               market_price=market_price)

    except Exception as e:
        return f"Error: {e}"

# API endpoint for AI FAQ (AJAX)
@app.route('/faq', methods=["POST"])
def faq():
    try:
        crop = request.json.get("crop")
        question = request.json.get("question")
        answer = get_gemini_faq_response(crop, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
