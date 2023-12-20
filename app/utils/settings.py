import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = os.path.join(os.getcwd(), ".env")
load_dotenv(f"{ENV_PATH}")


class AuthSettings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm:str = os.getenv("ALGORITHM")
    access_token_expires: int = os.getenv("TOKEN_EXPIRE_MINUTES")
    



class DatabaseSettings(BaseSettings):
    database : str = os.getenv("DATABASE")
    database_username : str = os.getenv("DATABASE_USERNAME")
    database_password : str = os.getenv("DATABASE_PASSWORD")
    database_hostname :str = os.getenv("DATABASE_HOSTNAME")
    database_name :str = os.getenv("DATABASE_NAME")
    database_port : int = os.getenv("DATABASE_PORT")




# all above in one class
class Settings(BaseSettings):
    database : str 
    database_username : str 
    database_password : str 
    database_hostname :str 
    database_name :str 
    database_port : int 
    secret_key: str 
    algorithm:str 
    access_token_expires: int 

    class Config:
        env_file = f"{ENV_PATH}"

