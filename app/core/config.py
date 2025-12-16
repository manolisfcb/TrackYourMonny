from dotenv import load_dotenv
from pydantic_settings import BaseSettings

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
        return f"sqlite:///./{self.APP_NAME.lower()}.db"
    
config = Config()