import os
import re
# import openai
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv() # Load environment variables from .env file

views = Blueprint("views", __name__)

# Load OpenAI API Key
# openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# models = genai.list_models()
# for model in models:
#     print(model.name)

def evaluate_password_strength(password):
    """Basic password strength analysis."""
    strength = {"length": False, "uppercase": False, "lowercase": False,
                "digits": False, "special_chars": False}

    if len(password) >= 8:
        strength["length"] = True
    if re.search(r'[A-Z]', password):
        strength["uppercase"] = True
    if re.search(r'[a-z]', password):
        strength["lowercase"] = True
    if re.search(r'\d', password):
        strength["digits"] = True
    if re.search(r'[@$!%*?&]', password):
        strength["special_chars"] = True

    score = sum(strength.values())
    
    if score == 5:
        rating = "Strong"
    elif score >= 3:
        rating = "Moderate"
    else:
        rating = "Weak"
    
    return {"password": password, "strength": rating, "criteria": strength}

def generate_password_advice(password):
    """Use Google Gemini API to provide password security advice."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"How secure is this password: {password}?")
        return response.text  # Return Gemini's response

    except Exception as e:
        return f"AI Error: {str(e)}"  # Return a user-friendly error message

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/check_password", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password", "")
    
    if not password:
        return jsonify({"error": "Password is required"}), 400
    
    strength_result = evaluate_password_strength(password)
    ai_advice = generate_password_advice(password)

    return jsonify({"strength": strength_result["strength"], "criteria": strength_result["criteria"], "advice": ai_advice})
