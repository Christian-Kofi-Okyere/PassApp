import json
import pytest
from unittest.mock import patch
from website.views import generate_password_advice

# Mock response for API failures
def fake_api_timeout(*args, **kwargs):
    raise TimeoutError("The request to Gemini API timed out.")

def fake_invalid_api_key(*args, **kwargs):
    raise ValueError("Invalid API key for Gemini API.")

def fake_generic_error(*args, **kwargs):
    raise Exception("Unexpected error from Gemini API.")

@patch("website.views.genai.GenerativeModel.generate_content", side_effect=fake_api_timeout)
def test_gemini_api_timeout(mock_gemini, client):
    """Test handling of Gemini API timeout."""
    response = client.post("/check_password",
                           data=json.dumps({"password": "P@ssword123"}),
                           content_type="application/json")
    
    data = response.get_json()
    
    assert response.status_code == 200
    assert "AI Error" in data["advice"]
    assert "timed out" in data["advice"]

@patch("website.views.genai.GenerativeModel.generate_content", side_effect=fake_invalid_api_key)
def test_gemini_invalid_api_key(mock_gemini, client):
    """Test handling of invalid API key error."""
    response = client.post("/check_password",
                           data=json.dumps({"password": "SecurePass123!"}),
                           content_type="application/json")

    data = response.get_json()
    
    assert response.status_code == 200
    assert "AI Error" in data["advice"]
    assert "Invalid API key" in data["advice"]

@patch("website.views.genai.GenerativeModel.generate_content", side_effect=fake_generic_error)
def test_gemini_generic_error(mock_gemini, client):
    """Test handling of unexpected Gemini API error."""
    response = client.post("/check_password",
                           data=json.dumps({"password": "StrongPass!2024"}),
                           content_type="application/json")

    data = response.get_json()
    
    assert response.status_code == 200
    assert "AI Error" in data["advice"]
    assert "Unexpected error" in data["advice"]
