import pytest
import os
import sys
from website import create_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(scope='module')
def app():
    """Create a test Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    yield app

@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()
