from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

# Load variables from .env into the environment
load_dotenv()
email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")


def send_email(to, subject, body):
    if not email_user or not email_pass:
        raise SystemExit("Missing EMAIL_USER or EMAIL_PASS. Check your .env file.")

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = email_user
        msg["To"] = to

        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)

    # Example usage
send_email("saifbayyari@protonmail.com", "Test Subject", "Hello, this is a test.")