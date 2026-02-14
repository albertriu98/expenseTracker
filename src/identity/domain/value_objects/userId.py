from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class UserId:
    value: UUID

    @staticmethod
    def new():
        return UserId(UUID())

    @property
    def value(self):
        return self._value