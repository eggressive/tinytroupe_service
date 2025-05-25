"""
Shared Flask extensions for TinyTroupe Service
"""
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
cors = CORS()

# These will be properly initialized with init_app later
