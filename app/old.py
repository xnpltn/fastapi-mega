import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
import time





app = FastAPI()









class Post(BaseModel):
    title: str
    content: str
    published: bool

my_posts = [
    {
        "id": 2,
        "title": "Post 1",
        "content": "Content 1",
    },
    {
        "id": 1,
        "title": "Post 2",
        "content": "Content 2",
    },
]

while True:
    try:
        connection = pg.connect(host="localhost", database="fastapi", user="postgres", password="qwerty", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print('database connection was success')
        break

    except Exception as err:
        print(err, 'connection failed')
        time.sleep(2)



def find_post(id):
    for post in my_posts:
        pass



@app.get("/")
def home():
    return {"date": "success"}





@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts ORDER BY "id" ASC""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

@app.post('/posts')
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ;""",(post.title, post.content, post.published))
    connection.commit()
    new_post = cursor.fetchone()
    return {"data": new_post }


@app.get("/posts/{id}")
def get_post(id: int):
    print(type(id))
    cursor.execute("""SELECT * FROM posts WHERE "id"= %s;""", str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return {"data": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE "id" = %s RETURNING * ;""", str(id))
    connection.commit()
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return {"data": post}



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET "title" = %s, "content" = %s, "published"= %s WHERE id = %s RETURNING *; """, (post.title, post.content, post.published, str(id)))
    connection.commit()
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return {"data": post}

