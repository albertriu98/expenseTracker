from dataclasses import dataclass
import uuid
from abc import ABC
from datetime import datetime

class Entity(ABC):
    pass

class AggregateRoot(Entity):
    pass

@dataclass(frozen=True)
class EntityId:
    value: uuid.UUID

    @staticmethod
    def new():
        return EntityId(uuid.uuid4())
    
    @property
    def value(self):
        return self._value

@dataclass(frozen=True)
class Event(ABC):
    datetime = datetime.now()