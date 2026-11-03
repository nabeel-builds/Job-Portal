from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models.user import User, UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=3, max_length=100)
    role: UserRole



class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime