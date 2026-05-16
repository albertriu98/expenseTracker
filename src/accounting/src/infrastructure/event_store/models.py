from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class Event(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )
    event_type: str
    payload: str
    published: bool = False
    published_at: datetime | None = None
