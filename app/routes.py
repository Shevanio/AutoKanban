from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db, socketio, login_manager
from app.models import User, Task
from app.automation import execute_automations, sync_google_calendar_task
from datetime import datetime
from app.forms import LoginForm
from app.automation import sync_google_calendar_task
from app import db, login_manager

def register_routes(app):
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('kanban'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.password_hash == form.password.data:  # O usa bcrypt.check_password_hash
                login_user(user)
                return redirect(url_for('kanban'))
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/kanban')
    @login_required
    def kanban():
        tasks = Task.query.filter_by(author_id=current_user.id).all()
        return render_template('kanban.html', tasks=tasks)

    @app.route('/add_task', methods=['POST'])
    @login_required
    def add_task():
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')  # Maneja conversión a datetime
        new_task = Task(title=title, description=description, author_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()

        # Sincroniza con Calendar
        sync_google_calendar_task(new_task)
        return redirect(url_for('kanban'))

    @app.route('/update_task/<int:task_id>/<new_status>')
    @login_required
    def update_task(task_id, new_status):
        task = Task.query.get_or_404(task_id)
        task.status = new_status
        db.session.commit()
        execute_automations(task)
        return jsonify({'status': 'success'})