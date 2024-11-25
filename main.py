from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randint

app = FastAPI()

my_posts = [
    {"title": "Favorite beaches", "content": "Puri, Seven mile, Eagle beach, Kannapali Beach", "id": 1},
    {"title": "Favorite Books", "content": "Harry potter series, Hunger games,", "id": 2},
    {"title": "Games for life", "content": "I will play AC series again and again", "id": 3}
]

class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to my Social Media Rest Api!!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(payload: Post):
    payload = payload.model_dump()
    payload["id"] = randint(4,10000)
    my_posts.append(payload)
    return{"data": my_posts}