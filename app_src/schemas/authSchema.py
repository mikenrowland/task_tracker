from email import message
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Register(BaseModel):
    email: EmailStr
    first_name: str = Field(..., max_length=60)
    last_name: Optional[str] = Field(..., max_length=60)
    password: str = Field(..., min_length=8, max_length=1500)


class RegisteredUser(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime


class SignInData(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=1500)

class SignInResponse(BaseModel):
    message: str
    token: str