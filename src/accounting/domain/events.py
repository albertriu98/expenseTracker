from dataclasses import dataclass
from src.accounting.domain.value_objects import Money

@dataclass(frozen=True)
class TransactionCommitted:
    account_id: str
    money: Money
    description: str
    transaction_type: str
    category_id: str = None