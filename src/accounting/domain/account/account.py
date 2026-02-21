from src.accounting.domain.account.accountId import AccountId
from src.accounting.domain.shared.domain_exceptions import InsufficientFundsException
from src.accounting.domain.account.money import Money
from src.accounting.domain.account.events import TransactionCommitted
from src.accounting.domain.transaction.transaction import Transaction

class Account:
    def __init__(self, initMoney: Money):
        self._accountId = AccountId.new()
        self._currency = initMoney.currency
        self._currentBalance = initMoney.amount
        self._dateCreated = datetime.now() #timestamp
        self._dateUpdated = datetime.now() #timestamp
        self._events = []
    
    @property
    def accountId(self):
        return self._accountId
    
    @property
    def currency(self):
        return self._currency
    
    @property
    def currentBalance(self):
        return self._currentBalance

    @property
    def dateCreated(self):
        return self._dateCreated
    
    @property
    def dateUpdated(self):
        return self._dateUpdated
    @property
    def events(self):
        return self._events

    def deposit(self, money: Money, description: str, categoryId: str):
        if self._currency != money.currency :
            raise InvalidCurrency("Transaction currency does not match with Account currency")
        transaction = Transaction.create_transaction(transaction_type="income" , 
                                                    account_id=self._accountId, 
                                                    amount=money.amount, 
                                                    currency=money.currency, 
                                                    description=description, 
                                                    categoryId=categoryId)
        self._currentBalance += transaction.money.amount
        self._events.append(TransactionCommitted(transaction_id=transaction.id, 
                                                account_id=transaction.accountId, 
                                                amount=transaction.amount,
                                                currency=transaction.currency, 
                                                transaction_type=transaction.transactionType,  
                                                category_id=transaction.categoryId))
        
    def withdraw(self, money: Money, description: str, categoryId: str):
        if self._currentBalance < money.amount :
            raise InsufficientFundsException("Not enough balance to withdraw.")
        elif self._currency != money.currency :
            raise InvalidCurrency("Transaction currency does not match with Account currency")
        transaction = Transaction.create_transaction(transaction_type: "expense" , 
                                                    account_id=self._accountId, 
                                                    amount=money.amount, 
                                                    currency=money.currency, 
                                                    description=description, 
                                                    categoryId=categoryId)
        self._currentBalance -= money.amount
        self._events.append(TransactionCommitted(transaction_id=transaction.id, 
                                                account_id=transaction.accountId, 
                                                amount=transaction.amount,
                                                currency=transaction.currency, 
                                                transaction_type=transaction.transactionType,  
                                                category_id=transaction.categoryId))

    @classmethod
    def openAccount(cls, initAmount: Money):
        return cls(initBalance=initAmount.amount, currency=initAmount.currency)

    