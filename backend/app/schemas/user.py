from pydantic import BaseModel, EmailStr, Field
from ..models.user import UserRole
from typing import Optional


class UserBase(BaseModel):
    """
    Base user model with common fields
    """
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    role: UserRole


class UserResponse(BaseModel):
    """
    User response model for API responses
    """
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="User's full name")
    email: Optional[str] = Field(None, description="User's email address")
    phone: Optional[str] = Field(None, description="User's phone number")
    role: str = Field(..., description="User role (citizen/officer/admin)")
    created_at: str = Field(..., description="Account creation timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "USR_ABC123",
                "name": "John Citizen",
                "email": "john@example.com",
                "phone": "+919876543210",
                "role": "citizen",
                "created_at": "2026-01-03T10:30:00Z"
            }
        }
