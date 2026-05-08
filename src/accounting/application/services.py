from src.accounting.domain.entities.account import Account
from src.accounting.domain.value_objects import MonetaryValue
from src.accounting.application.commands import CreateAccountCommand, CommitTransactionCommand
from src.accounting.domain.entities.transaction import Transaction
from src.accounting.infrastructure.repositories import AccountRepository, TransactionRepository
from src.accounting.infrastructure.event_store.event_store import EventStore

class AccountHandler:
    def __init__(self, account_repository: AccountRepository, event_store: EventStore):
        self.account_repository = account_repository
        self.event_store = event_store

    def create_account(self, aCommand: CreateAccountCommand):
        account = Account.create_account(aCommand.amount, aCommand.currency)
        try:
            self.account_repository.save(account)
            self.event_store.append(account.pull_events())  # Append events to the event store
        except Exception as e:
            # Handle the exception (e.g., log the error, rollback the transaction)
            raise e
        return account.accountId
    
    def commit_transaction(self, aCommand: CommitTransactionCommand):
        #Retrieve account by id
        account = self.account_repository.get_by_id(aCommand.accountId)
        try:
            if aCommand.transactionType == "income":
                account.deposit(MonetaryValue(aCommand.amount, aCommand.currency), aCommand.description, aCommand.category)
            elif aCommand.transactionType == "expense":
                account.withdraw(MonetaryValue(aCommand.amount, aCommand.currency), aCommand.description, aCommand.category)
            #Call event publisher to publish events in event store
            self.account_repository.save(account)
            self.event_store.append(account.pull_events())
        except Exception as e:
            # Handle the exception (e.g., log the error, rollback the transaction)
            raise e
        return  account.getCurrentBalance
    


