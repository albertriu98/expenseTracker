from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4

class Event(SQLModel, table=True):
    id: str = Field(primary_key=True)
    event_type: str
    payload: str
    published: bool = False
    published_at: datetime = None
