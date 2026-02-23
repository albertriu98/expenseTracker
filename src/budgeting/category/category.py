from src.domain.budgeting.categoryId import categroyId

class Category :
    def __init__(self, accountId: accountId, name: str, transactions: list(Transaction)):
        self._id = CategoryId.new()
        self._accountId = accountId
        self._name = name
        self._description = description

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
    def description(self):
        return self._description