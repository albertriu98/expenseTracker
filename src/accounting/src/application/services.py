from src.accounting.src.domain.entities.account import Account
from src.accounting.src.domain.value_objects import MonetaryValue
from src.accounting.src.application.commands import CreateAccountCommand, CommitTransactionCommand
from src.accounting.src.infrastructure.repositories.repositories import AccountRepository
from src.accounting.src.infrastructure.event_store.event_store import EventStore
from src.accounting.src.domain.domain_exceptions import InsufficientFundsException
from sqlmodel import Session

class AccountHandler:
    def __init__(self, session: Session):
        self.session = session
        self.account_repository = AccountRepository(session)
        self.event_store = EventStore(session)

    def create_account(self, aCommand: CreateAccountCommand):
        account = Account.create_account(aCommand.amount, aCommand.currency, aCommand.userId)
        self.account_repository.save(account)
        self.event_store.append(account.pull_events())  # Append events to the event store
        return account.accountId
    
    def commit_transaction(self, aCommand: CommitTransactionCommand):
        #Retrieve account by id
        account = self.account_repository.get_by_id(aCommand.accountId)
        if aCommand.transactionType == "income":
            account.deposit(MonetaryValue(aCommand.amount, aCommand.currency), aCommand.description, aCommand.category)
        elif aCommand.transactionType == "expense":
            try:
                account.withdraw(MonetaryValue(aCommand.amount, aCommand.currency), aCommand.description, aCommand.category)
            except InsufficientFundsException as e:
                raise e
        #Call event publisher to publish events in event store
        self.account_repository.save(account)
        self.event_store.append(account.pull_events())
        return  account.getCurrentBalance
    


