from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging
from ..auth.jwt import get_current_user
from ..db.mongo import get_database

router = APIRouter()
logger = logging.getLogger(__name__)

class FeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    feedback: Optional[str] = Field(None, description="Optional feedback text")

class FeedbackResponse(BaseModel):
    complaint_id: str
    rating: int
    feedback: Optional[str]
    submitted_at: datetime
    message: str

@router.post("/{complaint_id}/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    complaint_id: str,
    feedback_data: FeedbackRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Submit feedback for a resolved complaint
    """
    db = get_database()
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    
    # Get complaint
    complaint = await db.complaints.find_one({"complaint_id": complaint_id})
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Verify ownership
    if complaint.get("submitted_by") != current_user.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only submit feedback for your own complaints"
        )
    
    # Verify complaint is resolved
    if complaint.get("status") != "RESOLVED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only submit feedback for resolved complaints"
        )
    
    # Check if feedback already exists
    if complaint.get("feedback"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback already submitted for this complaint"
        )
    
    # Create feedback object
    feedback_obj = {
        "rating": feedback_data.rating,
        "feedback": feedback_data.feedback,
        "submitted_at": datetime.utcnow(),
        "submitted_by": current_user.get("user_id")
    }
    
    # Update complaint with feedback
    result = await db.complaints.update_one(
        {"complaint_id": complaint_id},
        {
            "$set": {
                "feedback": feedback_obj,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save feedback"
        )
    
    logger.info(f"Feedback submitted for complaint {complaint_id}: {feedback_data.rating} stars")
    
    return FeedbackResponse(
        complaint_id=complaint_id,
        rating=feedback_data.rating,
        feedback=feedback_data.feedback,
        submitted_at=feedback_obj["submitted_at"],
        message="Thank you for your feedback!"
    )

@router.get("/analytics/feedback-stats")
async def get_feedback_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    Get feedback statistics (admin only)
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    db = get_database()
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    
    # Aggregate feedback statistics
    pipeline = [
        {"$match": {"feedback": {"$exists": True}}},
        {"$group": {
            "_id": None,
            "total_feedback": {"$sum": 1},
            "avg_rating": {"$avg": "$feedback.rating"},
            "rating_distribution": {
                "$push": "$feedback.rating"
            }
        }}
    ]
    
    result = await db.complaints.aggregate(pipeline).to_list(1)
    
    if not result:
        return {
            "total_feedback": 0,
            "avg_rating": 0,
            "rating_distribution": {}
        }
    
    stats = result[0]
    
    # Calculate rating distribution
    rating_dist = {}
    for rating in stats.get("rating_distribution", []):
        rating_dist[rating] = rating_dist.get(rating, 0) + 1
    
    return {
        "total_feedback": stats.get("total_feedback", 0),
        "avg_rating": round(stats.get("avg_rating", 0), 2),
        "rating_distribution": rating_dist
    }
