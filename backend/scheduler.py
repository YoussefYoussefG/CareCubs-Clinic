import json
import os

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import Integer, cast
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from dotenv import load_dotenv

from database import SessionLocal
import models
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

load_dotenv()


def delete_last_year_appointments():
    """Delete all appointments from before the current year (runs annually on Jan 1)."""
    current_year = datetime.now().year
    last_year = current_year - 1
    try:
        session = SessionLocal()
        session.query(models.Appointment).filter(
            models.Appointment.appointmentDate < datetime(current_year, 1, 1)
        ).delete()
        session.commit()
        session.close()
        print(f"Deleted appointments from the year {last_year}")
    except SQLAlchemyError as e:
        print(f"An error occurred while deleting appointments: {e}")


def _get_firebase_credentials():
    """Load Firebase credentials from environment or file."""
    firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    scopes = ["https://www.googleapis.com/auth/firebase.messaging"]

    if firebase_creds_json:
        # Parse credentials from environment variable (preferred for deployment)
        creds_dict = json.loads(firebase_creds_json)
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=scopes
        )
    else:
        # Fall back to file (local development only)
        key_path = os.getenv("FIREBASE_KEY_PATH", "firebase_key.json")
        credentials = service_account.Credentials.from_service_account_file(
            key_path, scopes=scopes
        )

    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    return credentials.token


def send_notifications():
    """Check for upcoming appointments and send push notifications."""
    try:
        session = SessionLocal()
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d")
        two_hours_from_now = now + timedelta(hours=2)
        formatted_hour = two_hours_from_now.hour

        appointments = session.query(models.Appointment).filter(
            models.Appointment.appointmentDate == formatted_now,
            cast(models.Appointment.fromTime, Integer) <= formatted_hour,
        ).all()

        if not appointments:
            session.close()
            return

        for appointment in appointments:
            fcms = session.query(models.FCMToken).filter(
                models.FCMToken.userId == appointment.parentId
            ).all()
            _send_notification(appointment, fcms)

        session.close()
    except SQLAlchemyError as e:
        print(f"An error occurred while querying appointments: {e}")


def _send_notification(appointment, fcms):
    """Send FCM push notification to all registered devices."""
    try:
        access_token = _get_firebase_credentials()
    except Exception as e:
        print(f"Failed to get Firebase credentials: {e}")
        return

    fcm_project = os.getenv("FIREBASE_PROJECT_ID", "pulse-pediatric")

    for fcm in fcms:
        message = (
            f"You have an appointment scheduled on {appointment.appointmentDate} "
            f"from {appointment.fromTime} to {appointment.toTime}"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        payload = {
            "message": {
                "notification": {
                    "title": "Appointment Reminder",
                    "body": message,
                },
                "token": fcm.fcmToken,
            }
        }
        response = requests.post(
            f"https://fcm.googleapis.com/v1/projects/{fcm_project}/messages:send",
            headers=headers,
            json=payload,
        )
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print(f"Failed to send notification: {response.text}")


def start_scheduler():
    """Start the background scheduler for periodic tasks."""
    scheduler = BackgroundScheduler()
    # Delete old appointments on Jan 1 each year
    scheduler.add_job(
        delete_last_year_appointments, "cron",
        year="*", month="1", day="1", hour="0", minute="0",
    )
    # Check for upcoming appointments every minute
    scheduler.add_job(send_notifications, "cron", minute="*")
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
