from src.accounting.domain.entities.account import Account
from src.accounting.domain.entities.transaction import Transaction
from src.accounting.infrastructure.mappers import AccountMapper
from src.accounting.infrastructure.models import AccountModel, TransactionModel
from sqlmodel import SQLModel, Session, create_engine, select, update
from datetime import datetime

class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, account_id: str) -> Account:
        account = self.session.get(Account, account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        return AccountMapper.to_entity(account)

    def save(self, account: Account) -> None:
        model = AccountMapper.to_model(account)
        sql_account =self.session.get(AccountModel, account.accountId)
        if sql_account:
            if account.version != sql_account.version + 1:
                raise Exception("Concurrency conflict")
            self.session.merge(model)
        else:
            self.session.add(model)

        self.session.commit()
    
    def delete(self, account_id: str) -> None:
        account = self.session.get(AccountModel, account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        self.session.delete(account)
        self.session.commit()
  
class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id_and_account_id(self, transaction_id: str, account_id: str) -> Transaction:
        statement = select(Transaction).where(Transaction.id == transaction_id, Transaction.accountId == account_id)
        transaction = self.session.exec(statement).first()
        if not transaction:
            raise ValueError(f"Transaction with id {transaction_id} not found for account {account_id}")
        return transaction
    
    def get_all_by_account_id(self, account_id: str) -> list[Transaction]:
        statement = select(Transaction).where(Transaction.accountId == account_id)
        results = self.session.exec(statement).all()
        return results
    
    def get_by_time_range(self, account_id: str, start_date: datetime, end_date: datetime) -> list[Transaction]:
        statement = select(Transaction).where(
            Transaction.accountId == account_id,
            Transaction.dateCreated >= start_date,
            Transaction.dateCreated <= end_date
        )
        results = self.session.exec(statement).all()
        return results
    
    def  get_by_category_and_account_id(self, account_id: str, category_id: str) -> list[Transaction]:
        statement = select(Transaction).where(
            Transaction.accountId == account_id,
            Transaction.categoryId == category_id
        )
        results = self.session.exec(statement).all()
        return results

    def save(self, transaction: Transaction) -> None:
        sql_transaction = self.session.get(Transaction, transaction.id)
        if sql_transaction:
            if transaction.version != sql_transaction.version + 1:
                raise Exception("Concurrency conflict")
            self.session.merge(transaction)
        else:
            self.session.add(transaction)

        self.session.commit()

    def delete_by_account_id(self, account_id: str) -> None:
        statement = select(Transaction).where(Transaction.accountId == account_id)
        transactions = self.session.exec(statement).all()
        for transaction in transactions:
            self.session.delete(transaction)
        self.session.commit()