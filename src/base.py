from dataclasses import dataclass
import uuid
from abc import ABC
from datetime import datetime

class Entity(ABC):
    pass

@dataclass(frozen=True)
class Event(ABC):
    version: int

    def __post_init__(self):
        object.__setattr__(self, 'datetime', datetime.now())
        object.__setattr__(self, 'eventType', self.__class__.typeName)

    def to_dict(self) -> dict:
        """Serialize event to dictionary."""
        payload = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                payload[key] = value.isoformat()
            else:
                payload[key] = value
        eventType = self.__class__.typeName
        return {'eventType': eventType, 'payload': payload}


    @classmethod
    def from_dict(cls, data: dict):
        """Deserialize event from dictionary."""
        pass


class AggregateRoot(Entity):
    _events: list[Event]
    _version: int

    def __init__(self, version: int, events: list[Event] = []):
        self._events = events
        self._version = version
    
    @property
    def version(self):
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


        
