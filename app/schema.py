from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from typing_extensions import Annotated

class Todo(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int = None

class User(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: EmailStr

class TodoResponce(BaseModel):
    id: int
    title: str
    content: str
    # owner_id: int
    owner: UserOut



class UserLogin(User):
    ...
    

    
class UserResponce(BaseModel):
    email: EmailStr
    create_at: datetime

    class Config:
        # previously orm_mode = true
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    todo_id: int
    dir: Annotated[int, Field(ge=0, le=1) ]


class Resp(BaseModel):
    id: int
    published: bool
    content: str
    title: str
    owner_id: str
    created_at: datetime
    

class TodoOut(BaseModel):
    Todo: Resp
    votes: int

    class Config:
        orm_mode: True
