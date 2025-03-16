"""Module for creating and configuring the Flask application."""

import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Load environment variables from .env file.
    load_dotenv()

    # Set configuration from environment variables.
    app.config["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

    # Debug: Print the loaded GEMINI_API_KEY.
    print("Loaded GEMINI_API_KEY:", app.config["GEMINI_API_KEY"])

    # Import views inside the function to avoid circular imports.
    from .views import views  # pylint: disable=import-outside-toplevel
    app.register_blueprint(views, url_prefix="/")

    return app
