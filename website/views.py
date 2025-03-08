from flask import Blueprint, render_template, request, jsonify
import re

views = Blueprint("views", __name__)

def evaluate_password_strength(password):
    """Check password strength based on criteria."""
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

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/check_password", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password", "")
    
    if not password:
        return jsonify({"error": "Password is required"}), 400
    
    result = evaluate_password_strength(password)
    return jsonify(result)
