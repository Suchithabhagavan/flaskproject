"""
The flask application package.
"""
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# ------------------------------
# Configure Logging
# ------------------------------
# Create a file handler for logs (will also show in Azure Log Stream)
log_format = "%(asctime)s [%(levelname)s] - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

# Attach a handler to the app logger
file_handler = logging.StreamHandler()  # Azure captures stdout logs
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

app.logger.info("Flask application startup - logging initialized.")

# ------------------------------
# Configure Sessions, Database, Login
# ------------------------------
Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# ------------------------------
# Import Views
# ------------------------------
import FlaskWebProject.views
