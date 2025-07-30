from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdminBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "admin"
    permissions: Optional[str] = None

class AdminCreate(AdminBase):
    password_hash: str
    is_super_admin: bool = False
    is_active: bool = True

class AdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    permissions: Optional[str] = None
    is_super_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    last_login: Optional[datetime] = None

class AdminResponse(AdminBase):
    id: str
    is_super_admin: bool
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True