import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    
    # Load environment variables from .env
    load_dotenv()

    # Set configuration from environment variables
    app.config["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

    # Debugging: Print to check if the key is loaded
    print("Loaded GEMINI_API_KEY:", app.config["GEMINI_API_KEY"])

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app
