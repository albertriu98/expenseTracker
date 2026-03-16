
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class CategroyId:
    _value: UUID

    @staticmethod
    def new():
        return CategoryId(uuid4())
    
    @property
    def value(self):
        return self._value