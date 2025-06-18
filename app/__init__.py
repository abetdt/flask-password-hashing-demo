from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name='default'):
    """
    Application factory pattern
    """
    app = Flask(__name__)
    
    # Import and apply configuration
    from app.config.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models.user import User
    from app.models.service import Service
    
    # Register blueprints
    from app.views.auth import auth_bp
    from app.views.dashboard import dashboard_bp
    from app.views.services import services_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(services_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 