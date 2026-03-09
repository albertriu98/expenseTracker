from dataclasses import dataclass
import uuid

class Entity:
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