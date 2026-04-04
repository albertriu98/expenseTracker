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