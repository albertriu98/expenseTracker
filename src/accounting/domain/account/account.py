from src.accounting.domain.accountId import AccountId
from src.accounting.domain.shared.domain_exceptions import InsufficientFundsException

class Account:
    def __init__(self, currentBalance: float):
        self.accountId = AccountId.new()
        self._currentBalance = currentBalance
        
    
    def deposit(self, amount):
        self._current_balance += amount
        return "Deposit correctly performed"

    
    def withdraw(self, amount):
        if self._currentBalance < amount :
            raise InsufficientFundsException("Not enough balance to withdraw.")

    