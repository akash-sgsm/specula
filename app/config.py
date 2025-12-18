import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")
    # Lower threshold to catch more threats - can be tuned via .env
    THREAT_THRESHOLD = float(os.getenv("THREAT_THRESHOLD", "0.55"))
    DATABASE_PATH = os.getenv("DATABASE_PATH", "smart_cctv.db")
    # Alerts
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_FROM = os.getenv("TWILIO_FROM")
    ALERT_SMS_TO = os.getenv("ALERT_SMS_TO")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
