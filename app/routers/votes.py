from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..schema import Vote
from ..db import get_db
from ..utils.auth2 import get_current_user
from .. import models


router = APIRouter(
    prefix = "/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == vote.todo_id).first()
    if not todo_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sorry, todo not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.todo_id == vote.todo_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="user already liked this post")
        new_vote = models.Vote(todo_id = vote.todo_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"mesage": "liked post"} 
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote doesnt exist")  
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfull unvoted"}




