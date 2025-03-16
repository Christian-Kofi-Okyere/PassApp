"""Module for handling password evaluation and password advice generation
using Google Gemini API."""

import os
import re
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai  # pylint: disable=import-error

# Load environment variables from .env file
load_dotenv()

views = Blueprint("views", __name__)

# Configure the Gemini API using the key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_password_strength(password):
    """Perform basic password strength analysis."""
    strength = {
        "length": False,
        "uppercase": False,
        "lowercase": False,
        "digits": False,
        "special_chars": False
    }

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
    """Use Google Gemini API to provide password security advice for the given password."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"How secure is this password: {password}?")
        return response.text  # Return Gemini's response

    except Exception as e:  # pylint: disable=broad-exception-caught
        return f"AI Error: {str(e)}"  # Return a user-friendly error message

@views.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")

@views.route("/check_password", methods=["POST"])
def check_password():
    """Handle password checking and return strength analysis and AI advice."""
    data = request.get_json()
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    strength_result = evaluate_password_strength(password)
    ai_advice = generate_password_advice(password)

    return jsonify({
        "strength": strength_result["strength"],
        "criteria": strength_result["criteria"],
        "advice": ai_advice
    })
