import pytest
from website import create_app

@pytest.fixture
def app():
    """Create a test Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    yield app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()
