from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB


class Event(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )
    event_type: str
    payload: str
    published: bool = False
    published_at: datetime | None = None