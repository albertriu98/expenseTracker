from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4

class AccountModel(SQLModel, table=True):
    id: str = Field(primary_key=True)
    balance_amount: float
    balance_currency: str
    created_at: datetime 
    updated_at: datetime
    version: int

class TransactionModel(SQLModel, table=True):
    id: str = Field(primary_key=True)
    accountId: str = Field(foreign_key="accountmodel.id")
    transactionType: str
    money_amount: float
    money_currency: str
    description: str
    categoryId: str
    created_at: datetime 
    updated_at: datetime
    version: int