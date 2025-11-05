from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class ProductBase(BaseModel):
    name: str


class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ComplaintCreate(BaseModel):
    product_id: int
    description: str
    complaint_type_id: Optional[int] = None


class ComplaintRead(BaseModel):
    id: int
    description: str
    product: ProductRead
    predicted_label: Optional[str]
    score: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True
