import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_USER = os.getenv("API_USER")
    API_PASSWORD = os.getenv("API_PASSWORD")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "es")

settings = Settings()
