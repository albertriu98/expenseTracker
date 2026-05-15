from src.accounting.src.domain.entities.account import Account
from src.accounting.src.domain.value_objects import MonetaryValue
from src.accounting.src.domain.entities.transaction import Transaction
from src.accounting.src.infrastructure.repositories.models import AccountModel, TransactionModel

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
            balance_amount=entity.getCurrentBalance,
            balance_currency=entity.getCurrency,
            created_at=entity.dateCreated,
            updated_at=entity.dateUpdated,
            version=entity.version
        )

class TransactionMapper:
    @staticmethod
    def to_entity(model: TransactionModel) -> Transaction:
        return Transaction(
            transactionId=model.id,
            transactionType=model.transactionType,
            accountId=model.accountId,
            money=MonetaryValue(model.money_amount, model.money_currency),
            adescription=model.description,
            categoryId=model.categoryId,
            dateCreated=model.created_at,
            dateUpdated=model.updated_at,
            version=model.version
        )
    
    @staticmethod
    def to_model(entity: Transaction) -> TransactionModel:
        return TransactionModel(
            id=entity.id,
            transactionType=entity.transactionType.value,
            accountId=entity.accountId,
            money_amount=entity.amount,
            money_currency=entity.currency,
            description=entity.description,
            categoryId=entity.categoryId,
            created_at=entity.dateCreated,
            updated_at=entity.dateUpdated,
            version=entity.version
        )