from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Tokens de OAuth (JSON) para Gmail y Calendar
    gmail_token = db.Column(db.Text, nullable=True)
    google_calendar_token = db.Column(db.Text, nullable=True)

    # Relación con Task (un usuario -> muchas tasks)
    tasks = db.relationship('Task', backref='author', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='todo')
    due_date = db.Column(db.DateTime, nullable=True)
    calendar_event_id = db.Column(db.String(200), nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)