from typing_extensions import Annotated
from datetime import timedelta, datetime
from typing import Union

import pyotp

from email.message import EmailMessage
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse
from fastapi import Form, Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

import smtplib
from pydantic import EmailStr

from jose import jwt

from nzhinuFarm.config import settings
from nzhinuFarm import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


JWT_SECRET = settings.jwt_secret
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expires_minutes
COOKIE_NAME = settings.cookie_name

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def generateOTPCode(secret_code:str, duration):
    poy=  pyotp.TOTP(s=secret_code, interval=duration)
    return poy.now()


def create_access_token(user: schemas.User, 
                        expire_delta: Union[timedelta, None] = None):
    try:
        
        payload={
                "username":user.username,
                "email":user.email,
                "role":user.role,
            }
        
        if expire_delta:
            expire = datetime.utcnow() + expire_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        payload.update({"exp":expire})
        
        return jwt.encode(payload,key=JWT_SECRET, algorithm=ALGORITHM)
            
    except Exception as e:
        print(str(e))
        raise(e)
        

def sendmail_for_authentication(user_email:EmailStr, otp_code:str):
    email_address = settings.email_adress
    email_password = settings.email_password
    
    msg = EmailMessage()
    msg["Subject"] = "Authentication"
    msg["From"] = email_address
    msg["To"] = user_email 
    msg.set_content(f"Your OTP is {otp_code}. It expires after 60 seconds. Use it to authencicate")

    try:

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp :
            smtp.login(email_address, email_password)
            smtp.send_message(msg) 
        return JSONResponse(status_code=status.HTTP_200_OK, 
                            content={"Success":"Mail send successfully"})
    except Exception as e:
        print(e)



def send_mail_confirmation_creation(username:str, user_email:EmailStr):
    email_address = settings.email_adress
    email_password = settings.email_password
    
    msg = EmailMessage()
    msg["Subject"] = "Confirmation of creation of account"
    msg["From"] = email_address
    msg["To"] = user_email

    msg.set_content(f"Hello, {username}. Your account has been created successfully!") 

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address,email_password)
            smtp.send_message(msg)
            return JSONResponse(status_code=status.HTTP_200_OK, 
                                content={"Success": "The mail has been send successfully"})
    except Exception as e:
        print(e)


def get_user(db:Session, user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db:Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db:Session, skip:int = 0, limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user:schemas.UserCreate):
    db_user = models.User(username = user.username, role = user.role, 
                          email = user.email, password = hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db:Session, user_id:int):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    db.delete(user)
    db.commit()
    return user_id


def authenticate_user(db:Session, username:str=Form(), password:str=Form()):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with username {username} does not exists")
    if verify_password(password, user.password):
        return user
    else: 
        raise HTTPException(status_code=400, detail="Incorrect password")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        
        payload = jwt.decode(token=token, key=JWT_SECRET)
        print(payload)
        username = payload["username"]
        if username is None:
            raise credentials_exception
        
        return payload
    except Exception as e:
        print(e)


def create_user_item(db:Session, item:schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db:Session):
    return db.query(models.Item).all()

