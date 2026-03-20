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

    @classmethod
    def new(cls):
        return cls(uuid.uuid4())

@dataclass(frozen=True)
class Event(ABC):
    datetime = datetime.now()