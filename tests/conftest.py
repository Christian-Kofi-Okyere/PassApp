"""Pytest configuration module for setting up test fixtures."""

import pytest
from website import create_app


@pytest.fixture(scope="module")
def flask_app():
    """Create a test Flask app with testing configuration enabled."""
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture(scope="function")
def client(flask_app):
    """Create a test client using the Flask test client."""
    return flask_app.test_client()
