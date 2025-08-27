import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class DatabaseURI:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_NAME: str = os.getenv("DB_NAME")
    
    def get_uri(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = DatabaseURI().get_uri()


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = DatabaseURI(DB_NAME="flask_micro_test_db").get_uri()
    TESTING = True
