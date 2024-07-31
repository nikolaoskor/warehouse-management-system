from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    name: Optional[str] = Field(None, example="Sample Product")
    description: Optional[str] = Field(None, example="This is a sample product")
    price: Optional[float] = Field(None, example=9.99)
    stock: Optional[int] = Field(None, example=100)


class StockPayLoad(BaseModel):
    operation: str = Field(..., example="plus")
    stock: int = Field(..., example=10)
