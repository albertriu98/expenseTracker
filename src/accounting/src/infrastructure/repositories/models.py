from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID

class AccountModel(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    userId: str
    balance_amount: float
    balance_currency: str
    created_at: datetime 
    updated_at: datetime
    version: int

class TransactionModel(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    accountId: UUID = Field(foreign_key="accountmodel.id")
    transactionType: str
    money_amount: float
    money_currency: str
    description: str
    categoryId: str
    created_at: datetime 
    updated_at: datetime
    version: int