from sqlmodel import create_engine, Session, SQLModel
from os import getenv
from typing import Annotated
from fastapi import Depends
from src.accounting.infrastructure.repositories.models import AccountModel, TransactionModel
from src.accounting.infrastructure.event_store.models import Event

user = getenv("POSTGRESQL_USER")
password = getenv("POSTGRESQL_PASSWORD")
address = getenv("POSTGRESQL_ADDRESS")
database = getenv("POSTGRESQL_DATABASE_NAME")

engine = create_engine(f"postgresql://{user}:{password}@{address}/{database}")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]