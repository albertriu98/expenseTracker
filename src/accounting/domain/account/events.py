from dataclasses import dataclass
from src.accounting.domain.account.money import Money

@dataclass(frozen=True)
class TransactionCommitted:
    transaction_id: str
    account_id: str
    amount: Decimal
    currency: str
    transaction_type: str
    category_id: str = None