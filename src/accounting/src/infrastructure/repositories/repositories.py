from src.accounting.src.domain.entities.account import Account
from src.accounting.src.domain.entities.transaction import Transaction
from src.accounting.src.infrastructure.repositories.mappers import AccountMapper, TransactionMapper
from src.accounting.src.infrastructure.repositories.models import AccountModel, TransactionModel
from sqlmodel import Session, select
from datetime import datetime

class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, account_id: str) -> Account:
        account = self.session.get(AccountModel, account_id)
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

    
    def delete(self, account_id: str) -> None:
        account = self.session.get(AccountModel, account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        self.session.delete(account)

  
class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id_and_account_id(self, transaction_id: str, account_id: str) -> Transaction:
        statement = select(TransactionModel).where(TransactionModel.id == transaction_id, TransactionModel.accountId == account_id)
        transaction = self.session.exec(statement).first()
        if not transaction:
            raise ValueError(f"Transaction with id {transaction_id} not found for account {account_id}")
        return TransactionMapper.to_entity(transaction)
    
    def get_all_by_account_id(self, account_id: str) -> list[Transaction]:
        statement = select(TransactionModel).where(TransactionModel.accountId == account_id)
        results = self.session.exec(statement).all()
        return [TransactionMapper.to_entity(transaction) for transaction in results]
    
    def get_by_time_range(self, account_id: str, start_date: datetime, end_date: datetime) -> list[Transaction]:
        statement = select(TransactionModel).where(
            TransactionModel.accountId == account_id,
            TransactionModel.dateCreated >= start_date,
            TransactionModel.dateCreated <= end_date
        )
        results = self.session.exec(statement).all()
        return [TransactionMapper.to_entity(transaction) for transaction in results]
    
    def  get_by_category_and_account_id(self, account_id: str, category_id: str) -> list[Transaction]:
        statement = select(TransactionModel).where(
            TransactionModel.accountId == account_id,
            TransactionModel.categoryId == category_id
        )
        results = self.session.exec(statement).all()
        return [TransactionMapper.to_entity(transaction) for transaction in results]

    def save(self, transaction: Transaction) -> None:
        sql_transaction = self.session.get(TransactionModel, transaction.id)
        model =TransactionMapper.to_model(transaction)
        if sql_transaction:
            if transaction.version != sql_transaction.version + 1:
                raise Exception("Concurrency conflict")
            self.session.merge(model)
        else:
            self.session.add(model)

    def delete_by_account_id(self, account_id: str) -> None:
        statement = select(TransactionModel).where(TransactionModel.accountId == account_id)
        transactions = self.session.exec(statement).all()
        for transaction in transactions:
            self.session.delete(transaction)
