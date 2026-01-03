from pydantic import BaseModel, Field
from typing import Dict


class MetricsResponse(BaseModel):
    """
    System-wide metrics for admin dashboard
    """
    total_complaints: int = Field(..., description="Total number of complaints")
    status_counts: Dict[str, int] = Field(..., description="Count of complaints by status")
    category_counts: Dict[str, int] = Field(..., description="Count of complaints by category")
    average_resolution_hours: float = Field(..., description="Average time to resolve (hours)")
    backlog_size: int = Field(..., description="Number of unresolved complaints")
    urgency_distribution: Dict[str, int] = Field(..., description="Count by urgency level")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_complaints": 1543,
                "status_counts": {
                    "SUBMITTED": 23,
                    "TRIAGED": 15,
                    "ASSIGNED": 87,
                    "IN_PROGRESS": 142,
                    "RESOLVED": 1253,
                    "REJECTED": 23
                },
                "category_counts": {
                    "Utilities": 456,
                    "Sanitation": 321,
                    "Safety": 234,
                    "Health": 189,
                    "Education": 123,
                    "Administrative": 220
                },
                "average_resolution_hours": 18.5,
                "backlog_size": 267,
                "urgency_distribution": {
                    "HIGH": 45,
                    "MEDIUM": 156,
                    "LOW": 66
                }
            }
        }
