from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.complaint import ComplaintListResponse, UpdateStatusRequest
from ..db.mongo import get_database
from ..core.deps import get_current_officer
from ..models.complaint import ComplaintStatus, can_transition
from ..utils.time import utc_now
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/officer", tags=["Officer"])

@router.get("/inbox", response_model=List[ComplaintListResponse])
async def get_officer_inbox(current_user: dict = Depends(get_current_officer)):
    """
    Get all complaints assigned to this officer
    Sorted by urgency (HIGH first) then creation time
    """
    db = await get_database()
    
    urgency_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
    
    complaints = await db.complaints.find({
        "routing.assigned_officer_id": current_user["user_id"],
        "status": {"$nin": ["RESOLVED", "REJECTED"]}
    }).to_list(length=500)
    
    # Sort by urgency then time
    complaints.sort(
        key=lambda x: (
            urgency_order.get(x.get("triage", {}).get("urgency_level", "LOW"), 4),
            x["created_at"]
        )
    )
    
    return [
        ComplaintListResponse(
            complaint_id=c["complaint_id"],
            title=c["title"],
            status=c["status"],
            urgency_level=c.get("triage", {}).get("urgency_level"),
            created_at=c["created_at"],
            category=c.get("triage", {}).get("category")
        )
        for c in complaints
    ]

@router.patch("/complaints/{complaint_id}/status")
async def update_complaint_status(
    complaint_id: str,
    request: UpdateStatusRequest,
    current_user: dict = Depends(get_current_officer)
):
    """
    Update complaint status (officer/admin only)
    Enforces status transition rules
    """
    db = await get_database()
    
    complaint = await db.complaints.find_one({"complaint_id": complaint_id})
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Authorization: officer can only update assigned complaints, admin can update all
    if current_user["role"] == "officer":
        if complaint.get("routing", {}).get("assigned_officer_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your assigned complaints"
            )
    
    # Validate status transition
    current_status = complaint["status"]
    new_status = request.status.value
    
    if not can_transition(current_status, new_status):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status transition from {current_status} to {new_status}"
        )
    
    # Update complaint
    history_entry = {
        "status": new_status,
        "timestamp": utc_now(),
        "note": request.note,
        "updated_by": current_user["user_id"]
    }
    
    await db.complaints.update_one(
        {"complaint_id": complaint_id},
        {
            "$set": {
                "status": new_status,
                "updated_at": utc_now()
            },
            "$push": {"status_history": history_entry}
        }
    )
    
    logger.info(f"✅ Status updated: {complaint_id} -> {new_status}")
    
    return {"message": "Status updated successfully", "new_status": new_status}
