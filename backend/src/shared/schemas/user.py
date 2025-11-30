from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, EmailStr, Field

class UserRoleEnum(StrEnum):
    BUYER = "buyer"
    SELLER = "seller"
    SUPPLIER = "suplier"

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    role: UserRoleEnum = UserRoleEnum.BUYER
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    role: UserRoleEnum
    
    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
