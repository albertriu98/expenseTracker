from src.accounting.domain.entities.account import Account
from src.accounting.domain.value_objects import MonetaryValue
from src.accounting.application.commands import CreateAccountCommand, CommitTransactionCommand
from src.accounting.domain.entities.transaction import Transaction
from src.accounting.infrastructure.repositories import AccountRepository, TransactionRepository
from src.accounting.infrastructure.domain_event_publisher import RabbitMQEventPublisher

class AccountHandler:
    def __init__(self):
        self.account_repository = AccountRepository()
        self.event_publisher = RabbitMQEventPublisher()
    
    def create_account(self, aCommand: CreateAccountCommand):  
        account = Account.create_account(aCommand.amount, aCommand.currency)
        try:
            self.account_repository.save(account)
            #Call EventPublisher to publish events in event store
            self.event_publisher.publish(account.pull_events())
            return account.accountId
        except Exception as e:
            # Handle the exception (e.g., log the error, rollback the transaction)
            raise e
        
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
            self.event_publisher.publish(account.pull_events())
        except Exception as e:
            # Handle the exception (e.g., log the error, rollback the transaction)
            raise e
        return  account.getCurrentBalance
    


