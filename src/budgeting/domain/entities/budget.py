from src.budgeting.domain.value_objects import BudgetId, MonetaryValue
from src.budgeting.domain.value_objects import AccountId
from src.base import AggregateRoot

class Budget(AggregateRoot):
    def __init__(self, accountId: AccountId, name: str, moneyLImit: MonetaryValue, timeRange: timeRange, currency: str):
        super().__init__()
        self._id = BudgetId.new()
        self._accountId = accountId
        self._name = name
        self._moneyLimit = moneyLImit
        self._actualMoney = (0, currency)
        self._timeRange = timeRange
    
    @property
    def id(self):
        return self._id
    
    @property
    def accountId(self):
        return self._accountId
    
    @property
    def name(self):
        return self._name
    
    @property
    def moneyLimit(self):
        return self._moneyLimit
    
    @property
    def moneyLimit(self):
        return self._moneyLimit
    
    @property
    def actualMoney(self):
        return self._actualMoney
    
    @property
    def timeRange(self):
        return self.timeRange
    
