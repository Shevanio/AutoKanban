from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# Extensions
db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()

def create_app(config_class="config.DevelopmentConfig"):
    """Application factory for creating app instances."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Register blueprints or routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app