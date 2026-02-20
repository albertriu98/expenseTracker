from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class TransactionId:
    _value: UUID

    @staticmethod
    def new():
        return TransactionId(uuid4())
    
    @property
    def value(self):
        return self._value