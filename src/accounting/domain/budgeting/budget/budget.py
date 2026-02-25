class Budget:
    def __init__(self, accountId: accountId, name: str, moneyLImit: Money, timeRange: timeRange, categoryId: categoryId):
        self._id = BudgetId.new()
        self._accountId =
        self._name = name
        self._moneyLimit = moneyLImit
        self._actualMoney = 0
        self._timeRange = timeRange
        self._categoryId = categoryId
    
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
        return self._categoryId
    
    def accountTransaction(self):
        # Receive transaction (context mapping) and account it to actualMoney
        pass


    @classmethod
    def createBudget(cls, accountId, name, moneyLImit, timeRange, categoryId):
        return cls(accountId, name, moneyLImit, timeRange, categoryId)