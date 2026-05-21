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
