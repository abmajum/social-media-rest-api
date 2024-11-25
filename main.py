from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/")
def read_root():
    return {"message": "Welcome to my Social Media Rest Api!!"}

@app.get("/posts")
def get_posts():
    return {"data": "This is my post"}

@app.post("/createposts")
def create_posts(payload: Post):
    return{"title": payload.title , "content": payload.content}