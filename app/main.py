
from . import models
from .db import Base, engine, get_db
from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from .schema import Todo, TodoResponce, TodoOut
from passlib.context import CryptContext
from .utils.hash import pass_incryptor
from .routers import users, auth, votes
from .utils import auth2
from typing import List

app = FastAPI()


# CORS

origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# CORS









pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)




app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


#  response_model=List[TodoOut]

# @app.get("/todos", status_code=status.HTTP_200_OK, response_model=List[TodoResponce])
@app.get("/todos", status_code=status.HTTP_200_OK, )
def get_todos(id: int= None, db: Session = Depends(get_db)):
    # todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id)
    todos = db.query(models.Todo).all()
    if id:
        todos = db.query(models.Todo).filter(models.Todo.id == id)
    results = db.query(models.Todo, func.count(models.Vote.todo_id).label("votes")).join(models.Vote, models.Vote.todo_id == models.Todo.id, isouter=True).group_by(models.Todo.id).all()
    return results




@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    
    # new_post = models.Todo(title=todo.title, content=todo.content, published=todo.published)
    # print(current_user.email)
    if current_user is not None:
        todo.owner_id = current_user.id
        new_post = models.Todo(**todo.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return  new_post
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please login in ")

# response_model=TodoResponce
@app.get("/todos/{id}", status_code=status.HTTP_200_OK, response_model=TodoResponce)
def get_todo(id:int,  db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id==id).first()
    return todo

@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id:int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    
    todo = db.query(models.Todo).filter(models.Todo.id==id)
    if todo.first() is not None:
        if todo.first().owner_id  == current_user.id:
            todo.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="delete yours")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo doesnt exit")



@app.put("/todos/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(id:int, todo:Todo, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    
    todo_query = db.query(models.Todo).filter(models.Todo.id==id)
    if todo_query.first() is not None:
        if todo_query.first().owner_id  == current_user.id:
            update = todo.model_dump()
            update["owner_id"] = current_user.id
            todo_query.update(update, synchronize_session=False)
            db.commit()
            return todo_query.first()
            # return Response(status_code=status.HTTP_202_ACCEPTED)
            
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Updated yours")
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo doesnt exist")






