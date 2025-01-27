from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.login_view = 'routes_bp.login'  # Nombre del blueprint + la función .login

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    # Crear tablas si no existen
    with app.app_context():
        from app import models  # carga las clases
        db.create_all()

    # Registrar blueprint:
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
