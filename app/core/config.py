from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()


class Config(BaseSettings):
    APP_NAME: str = "TrackYourMonny"
    DEBUG: bool = False
    db_user: str = ""
    db_password: str = ""
    db_host: str = "localhost"
    db_name: str = "trackyourmonny"
    
    @property
    def database_url(self) -> str:
        return os.getenv("DATABASE_URL", f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}")
    
config = Config()