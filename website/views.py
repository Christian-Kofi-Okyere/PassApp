"""Module for handling password evaluation, advice generation, and secure password generation using Google Gemini API."""
import os
import re
import secrets
import string
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai  # pylint: disable=import-error

# Load environment variables from .env file
load_dotenv()

views = Blueprint("views", __name__)

# Configure the Gemini API using the key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_password_strength(password):
    """Perform enhanced password strength analysis."""
    strength = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digits": bool(re.search(r'\d', password)),
        "special_chars": bool(re.search(r'[@$!%*?&]', password))
    }

    # Check against a small list of common passwords
    common_passwords = {"password", "123456", "12345678", "qwerty", "abc123"}
    is_common = password.lower() in common_passwords

    score = sum(strength.values()) - (1 if is_common else 0)

    if is_common:
        rating = "Very Weak"
    elif score == 5:
        rating = "Strong"
    elif score >= 3:
        rating = "Moderate"
    else:
        rating = "Weak"

    return {"password": password, "strength": rating, "criteria": strength, "is_common": is_common}

def generate_password_advice(password):
    """Use Google Gemini API to provide password security advice for the given password."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Analyze the security of this password: {password} and provide advice on how to improve it."
        )
        return response.text  # Return Gemini's response
    except Exception as e:  # pylint: disable=broad-exception-caught
        return f"AI Error: {str(e)}"  # Return a user-friendly error message

def generate_random_password(length=12):
    """Generate a secure random password with letters, digits, and punctuation."""
    characters = string.ascii_letters + string.digits + "@$!%*?&"
    # Ensure the password meets criteria by including at least one of each required category
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("@$!%*?&")
    ]
    if length < 4:
        length = 4
    password += [secrets.choice(characters) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)

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
        "is_common": strength_result["is_common"],
        "advice": ai_advice
    })

@views.route("/generate_password", methods=["GET"])
def get_generated_password():
    """Endpoint to generate a secure random password."""
    length = request.args.get("length", 12, type=int)
    new_password = generate_random_password(length)
    return jsonify({"generated_password": new_password})
