from src.accounting.domain.entities.account import Account
from src.accounting.domain.value_objects import MonetaryValue
from src.accounting.application.commands import CreateAccountCommand
from src.accounting.domain.entities.transaction import Transaction
from src.accounting.infrastructure.repositories import AccountRepository, TransactionRepository

class CreateAccountHandler:
    def __init__(self):
        pass
    
    def create_account(self, aCommand: CreateAccountCommand):  
        account = Account.create_account(aCommand.amount, aCommand.currency)
        AccountRepository.save(account)
        #Call EventPublisher to publish events in event store
        return account.accountId
    
    def commit_transaction(self, aCommand: CommitTransactionCommand):
        #Retrieve account by id
        account = AccountRepository.get_by_id(aCommand.accountId)
        if aCommand.transactionType == "income":
            account.deposit(MonetaryValue(aCommand.amount, aCommand.currency), aCommand.description, aCommand.category)
        elif aCommand.transactionType == "expense":
            account.withdraw(MonetaryValue(aCommand.amount, aCommand.currency), aCommand.description, aCommand.category)
        #Call event publisher to publish events in event store
        AccountRepository.save(account)
        return  account.getCurrentBalance
    


