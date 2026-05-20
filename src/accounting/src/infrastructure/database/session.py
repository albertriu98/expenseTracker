from sqlmodel import create_engine, Session, SQLModel
from os import getenv
from typing import Annotated
from fastapi import Depends

user = getenv("DB_USER")
password = getenv("DB_PASSWORD")
host = getenv("DB_HOST")
port = getenv("DB_PORT", "5432")
database = getenv("DB_NAME")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]