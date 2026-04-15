from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        from_attributes = True