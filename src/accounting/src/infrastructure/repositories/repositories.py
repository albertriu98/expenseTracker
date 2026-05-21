from src.accounting.src.domain.entities.account import Account
from src.accounting.src.infrastructure.repositories.mappers import AccountMapper
from src.accounting.src.infrastructure.repositories.models import AccountModel
from sqlmodel import Session, select


class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, account_id: str) -> Account:
        account = self.session.get(AccountModel, account_id)
        if not account:
            return None
        return AccountMapper.to_entity(account)
    
    def get_by_userid(self, userid: str) -> Account:
        statement = select(AccountModel).where(AccountModel.userId == userid)
        account = self.session.exec(statement).first()
        if not account:
            return None
        return AccountMapper.to_entity(account)

    def save(self, account: Account) -> None:
        model = AccountMapper.to_model(account)
        sql_account =self.session.get(AccountModel, account.accountId.value)
        if sql_account:
            if account.version != sql_account.version + 1:
                raise Exception("Concurrency conflict")
            self.session.merge(model)
        else:
            self.session.add(model)

    def delete(self, account_id: str) -> None:
        account = self.session.get(AccountModel, account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        self.session.delete(account)
