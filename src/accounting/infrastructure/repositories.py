from src.accounting.domain.entities.account import Account
from src.accounting.domain.entities.transaction import Transaction
from sqlmodel import SQLModel, Session, create_engine, select, update

class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, account_id: str) -> Account:
        account = self.session.get(Account, account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        return account

    def save(self, account: Account) -> None:
        sql_account =self.session.get(Account, account.accountId)
        if sql_account:
            if account.version != sql_account.version - 1:
                raise Exception("Concurrency conflict")
            self.session.merge(account)
        else:
            self.session.add(account)

        self.session.commit()
    
    def delete_account(self, account_id: str) -> None:
        raise NotImplementedError
  