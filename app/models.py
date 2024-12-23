from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, text, DateTime
from typing import Union, Optional

class PostBase(SQLModel):
    title: str
    content: str
    published: bool = Field(sa_column_kwargs={"server_default": text("True"), "nullable": False})
    rating: Optional[int] = Field(default=None, nullable=True)

class Post(PostBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=None,sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()')))

class PostCreate(PostBase):
    pass

class PostPublic(PostBase):
    id: int
    created_at: datetime