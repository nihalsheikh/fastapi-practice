import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    origins = os.getenv("ORIGINS")
    db_url = os.getenv("DB_URL")
    secret_key = os.getenv("SECRET_KEY")

settings = Settings
