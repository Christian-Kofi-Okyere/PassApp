"""
Additional tests for website.views to improve coverage.
"""

import json
import re
from unittest.mock import patch

import pytest

from website import views


def test_evaluate_password_strength_strong():
    """
    Test evaluate_password_strength with a strong password.
    """
    password = "Str0ngP@ssw0rd!"
    result = views.evaluate_password_strength(password)
    criteria = result["criteria"]

    # Ensure all criteria are met
    assert criteria["length"] is True
    assert criteria["uppercase"] is True
    assert criteria["lowercase"] is True
    assert criteria["digits"] is True
    assert criteria["special_chars"] is True
    # Not in common password list
    assert result["is_common"] is False
    # Score should be 5, hence rating "Strong"
    assert result["strength"] == "Strong"


def test_evaluate_password_strength_common():
    """
    Test evaluate_password_strength with a common password.
    """
    password = "password"
    result = views.evaluate_password_strength(password)
    assert result["is_common"] is True
    # Even though criteria might be partially met, a common password is rated "Very Weak"
    assert result["strength"] == "Very Weak"


def test_generate_random_password_length_and_criteria():
    """
    Test generate_random_password to ensure it meets length requirements and contains
    at least one uppercase letter, one lowercase letter, one digit, and one special character.
    """
    def has_required_chars(pw):
        return (any(c.isupper() for c in pw) and
                any(c.islower() for c in pw) and
                any(c.isdigit() for c in pw) and
                any(c in "@$!%*?&" for c in pw))

    # Default length (12)
    default_password = views.generate_random_password()
    assert len(default_password) >= 12
    assert has_required_chars(default_password)

    # Custom length (e.g., 20)
    custom_password = views.generate_random_password(20)
    assert len(custom_password) >= 20
    assert has_required_chars(custom_password)


def test_home_route(client):
    """
    Test that the home ("/") route returns a 200 status code and renders content.
    """
    response = client.get("/")
    assert response.status_code == 200
    # In a test context the template rendering might be minimal; just ensure content exists.
    assert response.data


def test_get_generated_password_endpoint(client):
    """
    Test the /generate_password endpoint with and without a custom length parameter.
    """
    # Test default length
    response_default = client.get("/generate_password")
    data_default = response_default.get_json()
    assert response_default.status_code == 200
    assert "generated_password" in data_default
    assert len(data_default["generated_password"]) >= 12

    # Test with custom length (e.g., length=16)
    response_custom = client.get("/generate_password?length=16")
    data_custom = response_custom.get_json()
    assert response_custom.status_code == 200
    assert "generated_password" in data_custom
    assert len(data_custom["generated_password"]) >= 16


class FakeGeminiResponse:
    """
    A fake response object to simulate a successful Gemini API response.
    """
    def __init__(self, text):
        self.text = text


@patch("website.views.genai.GenerativeModel.generate_content")
def test_check_password_success(mock_generate_content, client):
    """
    Test the /check_password endpoint when Gemini API returns a successful response.
    """
    # Set up the fake API response
    fake_response = FakeGeminiResponse("Safe password advice")
    mock_generate_content.return_value = fake_response

    password = "Str0ngP@ssw0rd!"
    response = client.post(
        "/check_password",
        data=json.dumps({"password": password}),
        content_type="application/json"
    )
    data = response.get_json()
    assert response.status_code == 200

    # Verify that evaluate_password_strength works as expected
    assert data["strength"] == "Strong"
    # Check that the advice matches our fake response text
    assert data["advice"] == "Safe password advice"


def test_check_password_missing(client):
    """
    Test the /check_password endpoint when no password is provided.
    """
    response = client.post(
        "/check_password",
        data=json.dumps({}),
        content_type="application/json"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "error" in data
    assert data["error"] == "Password is required"
