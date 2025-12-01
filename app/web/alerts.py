import os
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText

class AlertManager:
    def __init__(self):
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from = os.getenv("TWILIO_FROM")
        self.sms_to = os.getenv("ALERT_SMS_TO")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_pass = os.getenv("SMTP_PASS")
        self.email_to = os.getenv("ALERT_EMAIL_TO")

    def send_sms(self, text):
        if not all([self.twilio_sid, self.twilio_token, self.twilio_from, self.sms_to]):
            return False
        client = Client(self.twilio_sid, self.twilio_token)
        client.messages.create(body=text, from_=self.twilio_from, to=self.sms_to)
        return True

    def send_email(self, subject, text):
        if not all([self.smtp_server, self.smtp_user, self.smtp_pass, self.email_to]):
            return False
        msg = MIMEText(text)
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = self.email_to
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as s:
            s.starttls()
            s.login(self.smtp_user, self.smtp_pass)
            s.send_message(msg)
        return True

    def send_manual_sos(self, message):
        self.send_sms(f"SOS: {message}")
        self.send_email("SOS Alert", message)

    def send_auto_alert(self, score, labels):
        text = f"Threat detected! Score={score:.2f}, Labels={','.join(labels)}"
        self.send_sms(text)
        self.send_email("Automatic Threat Alert", text)
