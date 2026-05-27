from src.accounting.src.domain.entities.account import Account
from src.accounting.src.domain.value_objects import MonetaryValue
from src.accounting.src.application.commands import CreateAccountCommand, CommitTransactionCommand
from src.accounting.src.infrastructure.repositories.repositories import AccountRepository
from src.accounting.src.infrastructure.event_store.event_store import EventStore
from src.accounting.src.domain.domain_exceptions import InsufficientFundsException
from sqlmodel import Session
from src.accounting.src.core.logging import logger

class AccountCommandHandler:
    def __init__(self, session: Session):
        self.session = session
        self.account_repository = AccountRepository(session)
        self.event_store = EventStore(session)

    def create_account(self, aCommand: CreateAccountCommand):
        account = self.account_repository.get_by_userid(aCommand.userId)
        if account:
            raise ValueError("Account already exists")
        logger.info(f"Creating account for userId: {aCommand.userId} with initial amount: {aCommand.amount} {aCommand.currency}")
        account = Account.create_account(aCommand.amount, aCommand.currency, aCommand.userId)
        logger.info(f"Account created with ID: {account.accountId.value}")
        logger.info(f"Persisting account....")
        self.account_repository.save(account)
        logger.info(f"Account persisted")
        logger.info(f"Appending events to event store...")
        self.event_store.append(account.pull_events())
        logger.info(f"Events appended to event store")
        self.session.commit()
        logger.info(f"Transaction committed to database")
        return account.accountId

    def commit_transaction(self, aCommand: CommitTransactionCommand):
        account = self.account_repository.get_by_id(aCommand.accountId)
        if not account:
            raise ValueError("Account not found")
        if aCommand.transactionType == "income":
            logger.info(f"Committing income transaction for accountId: {aCommand.accountId} with amount: {aCommand.amount} {aCommand.currency}")
            account.deposit(MonetaryValue(aCommand.amount, aCommand.currency), aCommand.description, aCommand.category)
        elif aCommand.transactionType == "expense":
            try:
                logger.info(f"Committing expense transaction for accountId: {aCommand.accountId} with amount: {aCommand.amount} {aCommand.currency}")
                account.withdraw(MonetaryValue(aCommand.amount, aCommand.currency), aCommand.description, aCommand.category)
            except InsufficientFundsException as e:
                logger.warning(f"Failed to commit transaction due to insufficient funds: {e}")
                raise e
        logger.info(f"Transaction committed to account. Current balance: {account.getCurrentBalance} {account.getCurrency}")
        logger.info(f"Persisting transaction....")
        self.account_repository.save(account)
        logger.info(f"Transaction persisted")
        logger.info(f"Appending events to event store...")
        self.event_store.append(account.pull_events())
        logger.info(f"Events appended to event store")
        self.session.commit()
        logger.info(f"Transaction committed to database")
        return account.getCurrentBalance
    
class AccountQueryHandler:
    def __init__(self, session: Session):
        self.session = session
        self.account_repository = AccountRepository(session)

    def get_balance(self, accountId: str):
        account = self.account_repository.get_by_id(accountId)
        if not account:
            raise ValueError("Account not found")
        return {"currentBalance": account.getCurrentBalance, "currency": account.getCurrency}


