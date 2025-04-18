"""Unit tests for password strength evaluation in website.views."""

import os
import sys
import pytest
from website.views import evaluate_password_strength
# Ensure the website package is discoverable before imports from 'website'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


@pytest.mark.parametrize("password, expected_strength", [
    ("12345", "Weak"),
    ("P@ssword", "Moderate"),
    ("StrongP@ssw0rd123!", "Strong"),
    ("", "Weak"),
    ("abcdef", "Weak"),
    ("Abc12345", "Moderate"),
])
def test_password_strength(password, expected_strength):
    """Test the password strength evaluation function."""
    result = evaluate_password_strength(password)
    assert result["strength"] == expected_strength
