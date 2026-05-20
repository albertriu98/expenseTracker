from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class userid:
    value: UUID

    @staticmethod
    def new():
        return userid(UUID())

    @property
    def value(self):
        return self._value