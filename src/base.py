from dataclasses import dataclass
import uuid
from abc import ABC
from datetime import datetime

class Entity(ABC):
    pass


class AggregateRoot(Entity):
    _events: list[Event]
    _version: int

    def __init__(self, version: int):
        self._events = []
        self._version = version
    
    @property
    def getVersion(self):
        return self._version

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
    def nextId(cls):
        return cls(uuid.uuid4())

@dataclass(frozen=True)
class Event(ABC):
    version: int

    def __post_init__(self):
        object.__setattr__(self, 'datetime', datetime.now())
        object.__setattr__(self, 'typeName', self.__class__.typeName)

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
        
