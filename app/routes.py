from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db, login_manager
from app.models import User, Task
from app.forms import LoginForm
from app.automation import sync_google_calendar_task
from app import bcrypt

# Crea el blueprint:
routes_bp = Blueprint('routes_bp', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@routes_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('routes_bp.kanban'))
    return redirect(url_for('routes_bp.login'))

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('routes_bp.kanban'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)

@routes_bp.route('/kanban')
@login_required
def kanban():
    tasks = Task.query.filter_by(author_id=current_user.id).all()
    return render_template('kanban.html', tasks=tasks)

@routes_bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    new_task = Task(title=title, description=description, author_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()

    # Sincroniza con Calendar
    sync_google_calendar_task(new_task)
    return redirect(url_for('routes_bp.kanban'))

@routes_bp.route('/update_task/<int:task_id>/<status>', methods=['GET', 'POST'])
@login_required
def update_task(task_id, status):
    # Buscar la tarea que pertenezca al usuario logueado
    task = Task.query.filter_by(id=task_id, author_id=current_user.id).first()
    if not task:
        return 'Tarea no encontrada', 404

    # Actualizar el estado
    task.status = status
    db.session.commit()

    # Si la tarea pasa a 'done', ejecuta automatizaciones
    if task.status == 'done':
        from app.automation import execute_automations
        execute_automations(task)

    return 'OK'

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes_bp.login'))
