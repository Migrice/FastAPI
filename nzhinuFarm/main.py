from typing import List
from datetime import timedelta
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from typing_extensions import Annotated

from pydantic import EmailStr
import pyotp

from nzhinuFarm import utils, models, schemas
from nzhinuFarm.database import SessionLocal, engine
from nzhinuFarm.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fast API DEMO", version="1.0")

class Tags(Enum):
    users = "User"
    items = "Item"
    token = "Token"
    login = "Login"

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    return {"Hello": "Welcome to my API"}

@app.get("/users/me", tags=[Tags.users])
async def read_users_me(current_user : 
    Annotated[schemas.User, Depends(utils.get_current_user)]):
    return current_user
        
@app.post("/users", response_model=schemas.User, tags=[Tags.users])
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="User with this email already exists")
    utils.send_mail_confirmation_creation(user.username, user.email)
    return utils.create_user(db=db, user=user)
 

@app.get("/users/", response_model=List[schemas.User], tags=[Tags.users])
def read_users(skip:int=0, limit:int=100,db:Session=Depends(get_db)):
    users = utils.get_users(db, skip,limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User,tags=[Tags.users])
def read_user(user_id:int, db:Session = Depends(get_db)):
    db_user = utils.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}",tags=[Tags.users])
def delete_user(user_id: int, db:Session=Depends(get_db)):
    user= utils.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not exists")
    user_del = utils.delete_user(db,user_id)
    return JSONResponse(content= f"User with id {str(user_del)} deleted successfully ", 
                        status_code=200)



@app.post("/token",tags=[Tags.token])
def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], 
          db:Session = Depends(get_db)):
    try:
        user = utils.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        access_token_expires = timedelta(minutes=settings.access_token_expires_minutes)
        access_token = utils.create_access_token(user,expire_delta=access_token_expires 
            )
        return {"access_token": access_token, "token_type": "bearer"}
            
    except Exception as e:
        print (e)
        raise HTTPException(status_code=400, detail="An error occured")
    

@app.post("/login",tags=[Tags.login])
def auth_user(email:EmailStr, db:Session=Depends(get_db)):
    user = utils.get_user_by_email(db,email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User with this email does not exists")
    otp = pyotp.TOTP(settings.otp_secret_key, interval=60)
    otp_code = otp.now()
    otp = otp_code
    try:

        utils.sendmail_for_authentication(email, otp_code)
        return JSONResponse(content="OTP code send successfully", status_code=200)
    except Exception as e:
        print(e)

@app.post("/items", tags=[Tags.items])
def create_item(item:schemas.ItemCreate, db:Session=Depends(get_db)):
    user = utils.get_user(db, item.owner_id)
    if not user:
        raise HTTPException(detail=f"User with id {item.owner_id} does not exists", 
                            status_code=400)
    try:
        item = utils.create_user_item(db, item)
        return item
    except Exception as e:
        print(e)

@app.get("/items", tags=[Tags.items], response_model=List[schemas.ItemBase])
def get_items(db:Session=Depends(get_db)):
    items = utils.get_items(db)
    return items

