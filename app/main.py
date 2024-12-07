from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randint
import psycopg
from psycopg.rows import dict_row
import os
import time

app = FastAPI()

my_posts = [
    {"title": "Favorite beaches", "content": "Puri, Seven mile, Eagle beach, Kannapali Beach", "id": 1, "published": True},
    {"title": "Favorite Books", "content": "Harry potter series, Hunger games,", "id": 2},
    {"title": "Games for life", "content": "I will play AC series again and again", "id": 3}
]


if not os.getenv("dbconnectionstring"):
    raise ValueError("The 'dbconnectionstring' environment variable must be set")
dbconnectionstring=os.getenv("dbconnectionstring")

while True:
    try:
        conn = psycopg.connect(conninfo=dbconnectionstring, row_factory=dict_row)
        cur = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection to the database failed!!!")
        print("Error:", error)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index(id):
    for i,post in enumerate(my_posts):
        if post['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"message": "Welcome to my Social Media Rest Api!!"}

@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts=cur.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_a_post(id: int):
    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return {"post detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Post):
    payload = payload.model_dump()
    payload["id"] = randint(4,10000)
    my_posts.append(payload)
    return{"data": my_posts}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesnot exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_a_post(id: int, post: Post):
    index = find_index(id=id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesnot exist")
    post = post.model_dump()
    db_post = my_posts[index]
    for k,v in post.items():
        db_post[k]= v
    my_posts[index] = db_post
    return {"message": f"post updated with id: {id}",
            "data": post
            }
