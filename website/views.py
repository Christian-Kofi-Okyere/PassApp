import os
import re
import openai
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

views = Blueprint("views", __name__)

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    """Use GPT-4 to provide personalized password security advice."""
    prompt = f"""
    The user entered the password: "{password}"
    
    Analyze its security risks and provide recommendations. 
    Suggest improvements if necessary. 
    Avoid disclosing the actual password in responses. 
    Ensure the advice is user-friendly and follows cybersecurity best practices.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a cybersecurity expert providing password security advice."},
                  {"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

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
