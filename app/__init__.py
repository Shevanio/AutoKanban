# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
# from flask_wtf.csrf import CSRFProtect
# from flask_login import LoginManager
# from app.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

# Extensions
db = SQLAlchemy()
login_manager = LoginManager()
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
    db.init_app(app)
    login_manager.init_app(app)  # Asegura que LoginManager está inicializado
    login_manager.login_view = "main.login"  # Página de inicio de sesión

    # Import models here to avoid circular imports
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints or routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app