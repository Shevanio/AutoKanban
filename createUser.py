from app import bcrypt
from app import db
from app.models import User

from app.forms import LoginForm

form = LoginForm()

hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
user = User(username=form.username.data, password_hash=hashed)
db.session.add(user)
db.session.commit()
