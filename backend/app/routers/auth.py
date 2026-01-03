from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas.auth import DemoLoginRequest, TokenResponse
from ..schemas.user import UserResponse
from ..db.mongo import get_database
from ..core.security import create_access_token
from ..utils.ids import generate_user_id
from ..utils.time import utc_now
from ..core.deps import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/demo-login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def demo_login(request: DemoLoginRequest):
    """
    Demo login endpoint for hackathon
    Creates a new user if not exists, returns JWT token
    
    **No password required** - simplified for demo purposes
    
    Args:
        request: DemoLoginRequest with name, role, optional email/phone
    
    Returns:
        TokenResponse: JWT access token and user information
    
    Example:
        ```json
        {
            "name": "John Citizen",
            "role": "citizen",
            "email": "john@example.com",
            "phone": "+919876543210"
        }
        ```
    """
    db = await get_database()
    
    # Check if user already exists (by name + role combination)
    user = await db.users.find_one({
        "name": request.name,
        "role": request.role.value
    })
    
    if not user:
        # Create new user
        user_id = generate_user_id()
        
        user_doc = {
            "user_id": user_id,
            "name": request.name,
            "email": request.email or f"{user_id.lower()}@demo.com",
            "phone": request.phone or "+919999999999",
            "role": request.role.value,
            "created_at": utc_now(),
            "updated_at": utc_now()
        }
        
        # Add department_id for officers
        if request.role.value == "officer":
            user_doc["department_id"] = None  # Will be assigned by admin
        
        result = await db.users.insert_one(user_doc)
        user = await db.users.find_one({"_id": result.inserted_id})
        
        logger.info(f"✅ New demo user created: {user_id} ({request.role.value})")
    else:
        logger.info(f"✅ Existing user logged in: {user['user_id']} ({user['role']})")
    
    # Create JWT token
    token_data = {
        "sub": user["user_id"],
        "role": user["role"],
        "name": user["name"]
    }
    
    access_token = create_access_token(token_data)
    
    # Prepare user response (remove MongoDB _id)
    user_response = {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user.get("email"),
        "phone": user.get("phone"),
        "role": user["role"],
        "created_at": user["created_at"]
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Requires: JWT token in Authorization header
    
    Returns:
        UserResponse: Current user details
    
    Example Authorization Header:
        ```
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
    """
    return UserResponse(
        user_id=current_user["user_id"],
        name=current_user["name"],
        email=current_user.get("email"),
        phone=current_user.get("phone"),
        role=current_user["role"],
        created_at=current_user["created_at"]
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Refresh JWT token for current user
    
    Requires: Valid JWT token in Authorization header
    
    Returns:
        TokenResponse: New JWT access token with extended expiry
    """
    # Create new token with same data
    token_data = {
        "sub": current_user["user_id"],
        "role": current_user["role"],
        "name": current_user["name"]
    }
    
    access_token = create_access_token(token_data)
    
    user_response = {
        "user_id": current_user["user_id"],
        "name": current_user["name"],
        "email": current_user.get("email"),
        "phone": current_user.get("phone"),
        "role": current_user["role"],
        "created_at": current_user["created_at"]
    }
    
    logger.info(f"✅ Token refreshed for user: {current_user['user_id']}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }
