# Dentro de venv, en la raíz del proyecto
#python
from app import create_app, db, bcrypt
from app.models import User
app = create_app()
ctx = app.app_context()
ctx.push()

# Crear un usuario
hashed_pw = bcrypt.generate_password_hash("mi_password").decode('utf-8')
u = User(username="david", email="david@example.com", password_hash=hashed_pw)
db.session.add(u)
db.session.commit()

# Verificar
u.password_hash
#'$2b$12$...'
