from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.forms import RegistrationForm, LoginForm, TaskForm
from app.models import User, Task
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=['GET'])
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all() if current_user.is_authenticated else []
    return render_template('home.html', tasks=tasks)

@main_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@main_bp.route("/create_task", methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            name=form.name.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            assigned_to_email=form.assigned_to_email.data,
            user_id=current_user.id,
            status='Pending',
            created_at=datetime.utcnow()
        )
        db.session.add(task)
        db.session.commit()
        flash('Task has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_task.html', title='Create Task', form=form)

@main_bp.route("/delete_task/<int:task_id>", methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('main.home'))
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted.', 'success')
    return redirect(url_for('main.home'))

@main_bp.route("/update_task/<int:task_id>", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('main.home'))
    form = TaskForm()
    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        task.start_time = form.start_time.data
        task.end_time = form.end_time.data
        task.assigned_to_email = form.assigned_to_email.data
        task.status = 'Updated'
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Task has been updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.name.data = task.name
        form.description.data = task.description
        form.start_time.data = task.start_time
        form.end_time.data = task.end_time
        form.assigned_to_email.data = task.assigned_to_email
    return render_template('update_task.html', title='Update Task', form=form)
