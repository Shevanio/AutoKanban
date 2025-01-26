from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db, socketio, login_manager
from app.models import User, Task
from app.automation import execute_automations, sync_google_calendar_task
from datetime import datetime

def register_routes(app):
    @app.route('/')
    def home():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form['email']).first()
            if user and user.password_hash == request.form['password']:
                login_user(user)
                return redirect(url_for('kanban'))
            flash('Credenciales incorrectas')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/kanban')
    @login_required
    def kanban():
        tasks = current_user.tasks
        return render_template('kanban.html', tasks=tasks)

    @app.route('/add_task', methods=['POST'])
    @login_required
    def add_task():
        due_date_str = request.form.get('due_date')
        due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
        task = Task(
            title=request.form['title'],
            description=request.form['description'],
            due_date=due_date,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        sync_google_calendar_task(task)
        return redirect(url_for('kanban'))

    @app.route('/update_task/<int:task_id>/<new_status>')
    @login_required
    def update_task(task_id, new_status):
        task = Task.query.get_or_404(task_id)
        task.status = new_status
        db.session.commit()
        execute_automations(task)
        return jsonify({'status': 'success'})