
from .. import models
from .. db import Base, engine, get_db
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..schema import  User, UserResponce
from ..utils.hash import pass_incryptor
from ..utils.auth2 import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)




@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponce)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is not None:
        return user
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
