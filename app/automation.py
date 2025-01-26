import base64
import json
from datetime import timedelta
from email.message import EmailMessage

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from app import db
from app.models import Task


def execute_automations(task):
    if task.status == 'done':
        send_email_notification(task)
        sync_google_calendar_task(task)


def get_gmail_service(user):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None

    # Intenta cargar credenciales existentes
    if user.gmail_token:
        info = json.loads(user.gmail_token)
        creds = Credentials.from_authorized_user_info(info, SCOPES)

    # Si no hay credenciales o no son válidas
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            SCOPES
        )
        # Solicitar acceso offline y forzar nueva autorización para obtener refresh_token
        creds = flow.run_local_server(
            port=5001,
            host='localhost',
            authorization_prompt_message='Abra esta URL en su navegador: {url}',
            success_message='Autenticación exitosa. Puede cerrar esta pestaña.',
            open_browser=True,
            access_type='offline',
            prompt='consent'
        )
        user.gmail_token = creds.to_json()
        db.session.commit()

    return build('gmail', 'v1', credentials=creds)


def send_email_notification(task):
    try:
        service = get_gmail_service(task.author)
        message = EmailMessage()
        message.set_content(f"Tarea completada: {task.title}\nDescripción: {task.description}")
        message['To'] = task.author.email
        message['Subject'] = f"✅ Tarea completada: {task.title}"

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
    except Exception as e:
        print(f"Error enviando email: {str(e)}")


def get_google_calendar_service(user):
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    creds = None

    # Intenta cargar credenciales existentes
    if user.google_calendar_token:
        info = json.loads(user.google_calendar_token)
        creds = Credentials.from_authorized_user_info(info, SCOPES)

    # Si no hay credenciales o no son válidas
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            SCOPES
        )
        # Solicitar acceso offline y forzar nueva autorización para obtener refresh_token
        creds = flow.run_local_server(
            port=5001,
            host='localhost',
            authorization_prompt_message='Abra esta URL en su navegador: {url}',
            success_message='Autenticación exitosa. Puede cerrar esta pestaña.',
            open_browser=True,
            access_type='offline',
            prompt='consent'
        )
        user.google_calendar_token = creds.to_json()  # Aquí ya debe venir el refresh_token
        db.session.commit()

    return build('calendar', 'v3', credentials=creds)


def sync_google_calendar_task(task):
    if task.due_date and not task.calendar_event_id:
        service = get_google_calendar_service(task.author)
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': task.due_date.isoformat(),
                'timeZone': 'Europe/Madrid'
            },
            'end': {
                'dateTime': (task.due_date + timedelta(hours=1)).isoformat(),
                'timeZone': 'Europe/Madrid'
            }
        }
        created_event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        task.calendar_event_id = created_event['id']
        db.session.commit()
