
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class UserId:
    _value: UUID

    @property
    def value(self):
        return self._value