#from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from pydantic import EmailStr


load_dotenv(verbose=True)

class Settings(BaseModel):
    jwt_secret:str = os.getenv("JWT_SECRET")
    db_url:str = os.getenv("SQLALCHEMY_DATABASE_URL")
    email_adress:EmailStr = os.getenv("EMAIL_ADRESS")
    email_password:str = os.getenv("EMAIL_PASSWORD")
    algorithm:str = os.getenv("ALGORITHM")
    access_token_expires_minutes:int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    cookie_name:int = os.getenv("COOKIE_NAME")
    postgres_user:str = os.getenv("POSTGRES_USER") 
    postgres_password:str = os.getenv("POSTGRES_PASSWORD")
    postgres_db:str = os.getenv("POSTGRES_DB")
    otp_secret_key:str = os.getenv("OTP_SECRET_KEY")
    

settings = Settings()
