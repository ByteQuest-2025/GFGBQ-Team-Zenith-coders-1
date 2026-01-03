from pydantic import BaseModel, Field, validator
from typing import Optional, List
from ..models.complaint import ComplaintStatus, UrgencyLevel


class LocationData(BaseModel):
    """
    Location information for a complaint
    """
    address: str = Field(..., min_length=5, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    ward: Optional[str] = None
    zone: Optional[str] = None
    
    @validator('longitude')
    def validate_coordinates(cls, v, values):
        """Ensure both lat and lng are provided together"""
        lat = values.get('latitude')
        if (lat is None) != (v is None):
            raise ValueError('Both latitude and longitude must be provided together')
        return v


class AttachmentData(BaseModel):
    """
    File attachment metadata
    """
    type: str = Field(..., description="Attachment type: image or audio")
    url: str = Field(..., description="Public URL of the uploaded file")


class TriageData(BaseModel):
    """
    AI triage results from NLP classification
    """
    category: Optional[str] = None
    category_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    urgency_level: Optional[str] = None
    urgency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    keywords_detected: List[str] = Field(default_factory=list)


class EscalationData(BaseModel):
    """
    Escalation information for high-priority complaints
    """
    needed: bool = False
    level: Optional[str] = None


class RoutingData(BaseModel):
    """
    Routing information - department and officer assignment
    """
    assigned_department: Optional[str] = None
    assigned_officer_id: Optional[str] = None
    assigned_officer_name: Optional[str] = None
    sla_hours: Optional[int] = Field(None, ge=1)
    escalation: EscalationData = Field(default_factory=EscalationData)


class StatusHistoryEntry(BaseModel):
    """
    Single entry in complaint status history
    """
    status: str = Field(..., description="Status value")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    note: str = Field(..., description="Status change note/reason")
    updated_by: Optional[str] = Field(None, description="User ID who made the update")


class ComplaintCreate(BaseModel):
    """
    Request model for creating a new complaint
    """
    title: str = Field(..., min_length=5, max_length=200, description="Brief complaint title")
    description: str = Field(..., min_length=10, max_length=2000, description="Detailed description")
    language: str = Field(default="auto", description="Language: auto/en/ta/hi")
    address: str = Field(..., min_length=5, max_length=500, description="Location address")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="GPS latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="GPS longitude")
    
    @validator('longitude')
    def validate_coordinates(cls, v, values):
        """Ensure both lat and lng are provided together"""
        lat = values.get('latitude')
        if (lat is None) != (v is None):
            raise ValueError('Both latitude and longitude must be provided together')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Broken streetlight on Main Road",
                "description": "The streetlight near shop #23 has not been working for 3 days causing safety issues at night",
                "language": "en",
                "address": "Main Road, Anna Nagar, Chennai - 600040",
                "latitude": 13.0843,
                "longitude": 80.2705
            }
        }


class ComplaintResponse(BaseModel):
    """
    Complete complaint response with all details
    """
    id: str = Field(..., description="MongoDB document ID")
    complaint_id: str = Field(..., description="Human-readable complaint ID")
    user_id: str = Field(..., description="User who created the complaint")
    title: str
    description: str
    language: str
    location: LocationData
    attachments: List[AttachmentData] = Field(default_factory=list)
    triage: TriageData
    routing: RoutingData
    status: str
    status_history: List[StatusHistoryEntry] = Field(default_factory=list)
    created_at: str
    updated_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "6795a1b2c3d4e5f678901234",
                "complaint_id": "COMP-2026-123456",
                "user_id": "USR_ABC123",
                "title": "Broken streetlight",
                "description": "Not working since 3 days",
                "language": "en",
                "location": {
                    "address": "Main Road, Chennai",
                    "latitude": 13.0843,
                    "longitude": 80.2705,
                    "ward": None,
                    "zone": None
                },
                "attachments": [],
                "triage": {
                    "category": "Utilities",
                    "category_confidence": 0.87,
                    "urgency_level": "MEDIUM",
                    "urgency_score": 0.62,
                    "keywords_detected": ["streetlight", "broken"]
                },
                "routing": {
                    "assigned_department": "DEPT_UTIL",
                    "assigned_officer_id": "USR_OFF001",
                    "assigned_officer_name": "Rajesh Kumar",
                    "sla_hours": 24,
                    "escalation": {"needed": False, "level": None}
                },
                "status": "ASSIGNED",
                "status_history": [
                    {
                        "status": "SUBMITTED",
                        "timestamp": "2026-01-03T10:00:00Z",
                        "note": "Complaint submitted"
                    }
                ],
                "created_at": "2026-01-03T10:00:00Z",
                "updated_at": "2026-01-03T10:01:00Z"
            }
        }


class ComplaintListResponse(BaseModel):
    """
    Simplified complaint model for list views
    """
    complaint_id: str
    title: str
    status: str
    urgency_level: Optional[str] = None
    created_at: str
    category: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "complaint_id": "COMP-2026-123456",
                "title": "Broken streetlight",
                "status": "ASSIGNED",
                "urgency_level": "MEDIUM",
                "created_at": "2026-01-03T10:00:00Z",
                "category": "Utilities"
            }
        }


class UpdateStatusRequest(BaseModel):
    """
    Request model for updating complaint status (officer/admin)
    """
    status: ComplaintStatus = Field(..., description="New status")
    note: str = Field(..., min_length=5, max_length=500, description="Reason for status update")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "IN_PROGRESS",
                "note": "Team dispatched to location. Expected resolution in 4 hours."
            }
        }
