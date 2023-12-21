from .. import models
from .. db import get_db
from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schema import  User, UserLogin, UserResponce
from ..utils.hash import pass_incryptor, verify_password
from .. utils.auth2 import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/signup", response_model=UserResponce, status_code=status.HTTP_201_CREATED)
def signup(user: User, db: Session = Depends(get_db)):

    user.password = pass_incryptor(user.password)
    user_query = db.query(models.User).filter(models.User.email == user.email).first()
    if user_query is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with that email already exits")
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user



@router.post("/login")
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify_password(user_creds.password, user_query.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # CREATE TOKEN
    access_token = create_access_token(data={"user_id": user_query.id})
    
    
    return  {
        "token": access_token,
        "token_type": "Bearer",
    }