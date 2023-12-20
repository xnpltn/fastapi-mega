from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..schema import TokenData
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer as pwb
from .. db import get_db
from sqlalchemy.orm import Session
from .. import models
from .settings import Settings

settings = Settings()

# # SECRET_KEY
# SECRET_KEY = "10055b9168af2eb9f398e6cfc96d16b2259f3887359d3a8f1710dafd2ae20f23"
# # ALGORITH
# ALGORITHM = "HS256"
# # EXPIRETIION tIME
# ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict ,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expires)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expires)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    # print(encoded_jwt)
    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)
    except JWTError as exc:
        raise credential_exception
    return token_data

def get_current_user(token:str = Depends(pwb(tokenUrl="login")), db : Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token =  verify_access_token(token=token, credential_exception=credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

