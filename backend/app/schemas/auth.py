from pydantic import BaseModel, Field
from ..models.user import UserRole
from typing import Optional


class DemoLoginRequest(BaseModel):
    """
    Request model for demo login endpoint
    No password required - simplified for hackathon
    """
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    role: UserRole = Field(..., description="User role: citizen, officer, or admin")
    email: Optional[str] = Field(None, description="Optional email address")
    phone: Optional[str] = Field(None, description="Optional phone number")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Citizen",
                "role": "citizen",
                "email": "john@example.com",
                "phone": "+919876543210"
            }
        }


class TokenResponse(BaseModel):
    """
    Response model for authentication endpoints
    Contains JWT token and user information
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    user: dict = Field(..., description="User information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "user_id": "USR_ABC123",
                    "name": "John Citizen",
                    "role": "citizen",
                    "email": "john@example.com"
                }
            }
        }
