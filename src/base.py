from dataclasses import dataclass
import uuid
from abc import ABC
from datetime import datetime

class Entity(ABC):
    version: int

    def __init__(self):
        self.version = 0


class AggregateRoot(Entity):
    super().__init__()

    _events: list[Event]

    def __init__(self):
        self._events = []

    def pull_events(self):
        events = self._events[:]
        self._events.clear()
        return events
    
    def add_event(self, event: Event):
        self._events.append(event)

@dataclass(frozen=True)
class EntityId:
    value: uuid.UUID

    @classmethod
    def new(cls):
        return cls(uuid.uuid4())

@dataclass(frozen=True)
class Event(ABC):
    datetime = datetime.now()
    version: int
    typeName: str

    def to_dict(self) -> dict:
        """Serialize event to dictionary."""
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            else:
                data[key] = value
        return data


    @classmethod
    def from_dict(cls, data: dict):
        """Deserialize event from dictionary."""
        
