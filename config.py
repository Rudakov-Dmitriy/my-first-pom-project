import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")

settings = Settings()