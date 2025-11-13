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
app = Flask(_name_)
app.config.from_object(Config)

# ------------------------------
# Configure Logging
# ------------------------------
log_format = "%(asctime)s [%(levelname)s] - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

file_handler = logging.StreamHandler()  # Azure captures STDOUT logs
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
# Import routes
# ------------------------------
# (kept at end to avoid circular imports)
import FlaskWebProject.views
