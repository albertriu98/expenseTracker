from src.accounting.src.domain.entities.account import Account
from src.accounting.src.domain.value_objects import MonetaryValue, AccountId
from src.accounting.src.infrastructure.repositories.models import AccountModel

class AccountMapper:
    @staticmethod
    def to_entity(model: AccountModel) -> Account:
        return Account(
            accountId=AccountId(model.id),
            userId=model.userId,
            aBalance=MonetaryValue(model.balance_amount, model.balance_currency),
            dateCreated=model.created_at,
            dateUpdated=model.updated_at,
            version=model.version
        )
    
    @staticmethod
    def to_model(entity: Account) -> AccountModel:
        return AccountModel(
            id=entity.accountId.value,
            userId=entity.userId,
            balance_amount=entity.getCurrentBalance,
            balance_currency=entity.getCurrency,
            created_at=entity.dateCreated,
            updated_at=entity.dateUpdated,
            version=entity.version
        )
