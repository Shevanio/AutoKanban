from flask import current_app, render_template
from app.models import Task
from app import db, mail
from flask_mail import Message
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

def perform_automation_task(task_name):
    """Executes the specified automation task, synchronizes with Google Calendar, and sends an email notification."""
    try:
        with current_app.app_context():
            # Retrieve the task from the database
            task = Task.query.filter_by(name=task_name).first()
            if not task:
                raise ValueError(f"Task {task_name} not found in the database.")

            # Update task status to 'In Progress'
            task.status = "In Progress"
            task.updated_at = datetime.datetime.utcnow()
            db.session.commit()
            current_app.logger.info(f"Starting task: {task_name}")

            # Synchronize with Google Calendar
            credentials = service_account.Credentials.from_service_account_file(
                'path/to/credentials.json',
                scopes=['https://www.googleapis.com/auth/calendar']
            )
            service = build('calendar', 'v3', credentials=credentials)

            event = {
                'summary': task_name,
                'description': task.description,
                'start': {
                    'dateTime': task.start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': task.end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }

            calendar_id = 'primary'
            service.events().insert(calendarId=calendar_id, body=event).execute()
            current_app.logger.info(f"Task {task_name} added to Google Calendar.")

            # Send email notification
            msg = Message(
                subject=f"Task Update: {task_name}",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[task.assigned_to_email]
            )
            msg.body = render_template('email/task_notification.txt', task=task)
            msg.html = render_template('email/task_notification.html', task=task)
            mail.send(msg)
            current_app.logger.info(f"Email notification sent for task: {task_name}.")

            # Update task status to 'Completed'
            task.status = "Completed"
            task.updated_at = datetime.datetime.utcnow()
            db.session.commit()

            return f"Task {task_name} executed successfully."

    except Exception as e:
        current_app.logger.error(f"Error performing task {task_name}: {e}")
        return f"Failed to perform task {task_name}."