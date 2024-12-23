import os
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends
from typing_extensions import Annotated

if not os.getenv("dbconnectionstring"):
    raise ValueError("The 'dbconnectionstring' environment variable must be set")
dbconnectionstring=os.getenv("dbconnectionstring")

engine = create_engine(dbconnectionstring)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    create_db_and_tables()
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]



