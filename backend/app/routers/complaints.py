from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import Optional, List
from datetime import datetime
import logging
from ..auth.jwt import get_current_user
from ..db.mongo import get_database
from ..schemas.complaint import ComplaintCreate, ComplaintResponse
from ..ai.triage import triage_engine
from ..services.routing_service import routing_service
from ..services.notification_service import notification_service
from ..services.duplicate_detector import duplicate_detector

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def create_complaint(
    title: str = Form(...),
    description: str = Form(...),
    address: str = Form(...),
    language: str = Form("auto"),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new complaint with AI triage and duplicate detection
    """
    db = get_database()
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    
    # Generate complaint ID
    complaint_count = await db.complaints.count_documents({})
    complaint_id = f"CMP{str(complaint_count + 1).zfill(6)}"
    
    # Prepare complaint data
    complaint_data = {
        "complaint_id": complaint_id,
        "title": title,
        "description": description,
        "location": {
            "address": address,
            "latitude": latitude,
            "longitude": longitude
        },
        "language": language,
        "status": "SUBMITTED",
        "submitted_by": current_user.get("user_id"),
        "submitted_by_email": current_user.get("email"),
        "submitted_by_phone": current_user.get("phone"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "status_history": [{
            "status": "SUBMITTED",
            "timestamp": datetime.utcnow(),
            "note": "Complaint submitted"
        }]
    }
    
    # Handle image upload if provided
    if image:
        # Save image logic here
        image_path = f"uploads/{complaint_id}_{image.filename}"
        complaint_data["image_url"] = image_path
    
    # Check for duplicates
    try:
        existing_complaints = await db.complaints.find({
            "status": {"$in": ["SUBMITTED", "TRIAGED", "ASSIGNED", "IN_PROGRESS"]}
        }).to_list(100)
        
        duplicate_check = duplicate_detector.check_for_duplicates(
            complaint_data,
            existing_complaints
        )
        
        complaint_data["duplicate_check"] = duplicate_check
        
        if duplicate_check.get("is_duplicate"):
            logger.info(f"Potential duplicate detected for {complaint_id}")
            complaint_data["is_potential_duplicate"] = True
            
    except Exception as e:
        logger.error(f"Duplicate detection failed: {e}")
        complaint_data["duplicate_check"] = {
            "is_duplicate": False,
            "duplicate_count": 0,
            "similar_complaints": []
        }
    
    # AI Triage
    try:
        triage_result = triage_engine.triage_complaint(
            title=title,
            description=description,
            language=language
        )
        
        complaint_data["category"] = triage_result["category"]
        complaint_data["urgency_level"] = triage_result["urgency_level"]
        complaint_data["triage"] = triage_result
        complaint_data["status"] = "TRIAGED"
        
        complaint_data["status_history"].append({
            "status": "TRIAGED",
            "timestamp": datetime.utcnow(),
            "note": f"AI classified as {triage_result['category']} - {triage_result['urgency_level']} urgency"
        })
        
    except Exception as e:
        logger.error(f"Triage failed: {e}")
        complaint_data["category"] = "Administrative"
        complaint_data["urgency_level"] = "MEDIUM"
    
    # Smart Routing
    try:
        routing_result = routing_service.assign_officer(
            complaint_data,
            await db.officers.find().to_list(100)
        )
        
        if routing_result:
            complaint_data["routing"] = routing_result
            complaint_data["assigned_to"] = routing_result["assigned_officer_id"]
            complaint_data["status"] = "ASSIGNED"
            
            complaint_data["status_history"].append({
                "status": "ASSIGNED",
                "timestamp": datetime.utcnow(),
                "note": f"Assigned to {routing_result['assigned_officer_name']}"
            })
            
            # Notify officer
            try:
                officer = await db.officers.find_one({"officer_id": routing_result["assigned_officer_id"]})
                if officer:
                    notification_service.notify_officer_assignment(
                        complaint_data,
                        officer.get("email"),
                        officer.get("name")
                    )
            except Exception as e:
                logger.error(f"Failed to notify officer: {e}")
                
    except Exception as e:
        logger.error(f"Routing failed: {e}")
    
    # Save to database
    result = await db.complaints.insert_one(complaint_data)
    
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create complaint"
        )
    
    # Send notification to citizen
    try:
        notification_service.notify_complaint_submitted(
            complaint_data,
            current_user.get("email"),
            current_user.get("phone")
        )
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
    
    logger.info(f"Complaint {complaint_id} created successfully")
    
    return complaint_data

@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get complaint details by ID
    """
    db = get_database()
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    
    complaint = await db.complaints.find_one({"complaint_id": complaint_id})
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Check access permissions
    user_role = current_user.get("role")
    if user_role == "citizen" and complaint.get("submitted_by") != current_user.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return complaint

@router.get("", response_model=List[ComplaintResponse])
async def get_complaints(
    status: Optional[str] = None,
    category: Optional[str] = None,
    urgency: Optional[str] = None,
    mine: Optional[bool] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get complaints with filters
    """
    db = get_database()
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    
    query = {}
    
    # Apply filters
    if status:
        query["status"] = status
    if category:
        query["category"] = category
    if urgency:
        query["urgency_level"] = urgency
    
    # Filter by current user for citizens
    if current_user.get("role") == "citizen" or mine:
        query["submitted_by"] = current_user.get("user_id")
    
    complaints = await db.complaints.find(query).sort("created_at", -1).to_list(100)
    
    return complaints

@router.put("/{complaint_id}/status")
async def update_complaint_status(
    complaint_id: str,
    status: str,
    note: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Update complaint status (officer/admin only)
    """
    db = get_database()
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    
    # Verify permissions
    if current_user.get("role") not in ["officer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only officers and admins can update status"
        )
    
    complaint = await db.complaints.find_one({"complaint_id": complaint_id})
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Update status
    status_entry = {
        "status": status,
        "timestamp": datetime.utcnow(),
        "updated_by": current_user.get("user_id"),
        "note": note
    }
    
    result = await db.complaints.update_one(
        {"complaint_id": complaint_id},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            },
            "$push": {
                "status_history": status_entry
            }
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update status"
        )
    
    # Send notifications
    try:
        if status == "RESOLVED":
            notification_service.notify_complaint_resolved(
                complaint,
                complaint.get("submitted_by_email"),
                complaint.get("submitted_by_phone")
            )
        else:
            notification_service.notify_status_updated(
                complaint,
                complaint.get("submitted_by_email"),
                status,
                note,
                complaint.get("submitted_by_phone")
            )
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
    
    logger.info(f"Complaint {complaint_id} status updated to {status}")
    
    return {"message": "Status updated successfully", "complaint_id": complaint_id, "new_status": status}
