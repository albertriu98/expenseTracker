from src.accounting.domain.entities.account import Account
from src.accounting.domain.value_objects import MonetaryValue
from src.accounting.domain.entities.transaction import Transaction
from src.accounting.infrastructure.models import AccountModel, TransactionModel

class AccountMapper:
    @staticmethod
    def to_entity(model: AccountModel) -> Account:
        return Account(
            accountId=model.id,
            currentBalance=MonetaryValue(model.balance_amount, model.balance_currency),
            dateCreated=model.created_at,
            dateUpdated=model.updated_at,
            version=model.version
        )
    
    @staticmethod
    def to_model(entity: Account) -> AccountModel:
        return AccountModel(
            id=entity.id,
            balance_amount=entity.balance_amount,
            balance_currency=entity.balance_currency,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            version=entity.version
        )