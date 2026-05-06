from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4

class Event(SQLModel, table=True):
    id: str = Field(primary_key=True)
    aggregate_id: str
    event_type: str
    created_at: datetime
    payload: str
    published: bool = False
    published_at: datetime | None = None
