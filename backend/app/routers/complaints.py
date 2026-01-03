from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from typing import List, Optional
from ..schemas.complaint import ComplaintCreate, ComplaintResponse, ComplaintListResponse
from ..db.mongo import get_database
from ..core.deps import get_current_user, get_current_citizen
from ..utils.ids import generate_complaint_id
from ..utils.time import utc_now
from ..services.file_storage import file_storage_service
from ..services.triage_client import triage_client
from ..services.routing_service import routing_service
from ..models.complaint import ComplaintStatus
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/complaints", tags=["Complaints"])

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_complaint(
    title: str = Form(...),
    description: str = Form(...),
    language: str = Form("auto"),
    address: str = Form(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new complaint (citizen only)
    Accepts multipart/form-data with optional image/audio attachments
    """
    
    # Validate location data
    if (latitude is None) != (longitude is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both latitude and longitude must be provided together"
        )
    
    db = await get_database()
    complaint_id = generate_complaint_id()
    
    # Handle file uploads
    attachments = []
    if image:
        image_url = await file_storage_service.save_file(image, "image")
        attachments.append({"type": "image", "url": image_url})
    
    if audio:
        audio_url = await file_storage_service.save_file(audio, "audio")
        attachments.append({"type": "audio", "url": audio_url})
    
    # Create complaint document
    complaint_doc = {
        "complaint_id": complaint_id,
        "user_id": current_user["user_id"],
        "title": title,
        "description": description,
        "language": language,
        "location": {
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "ward": None,
            "zone": None
        },
        "attachments": attachments,
        "triage": {
            "category": None,
            "category_confidence": None,
            "urgency_level": None,
            "urgency_score": None,
            "keywords_detected": []
        },
        "routing": {
            "assigned_department": None,
            "assigned_officer_id": None,
            "assigned_officer_name": None,
            "sla_hours": None,
            "escalation": {"needed": False, "level": None}
        },
        "status": ComplaintStatus.SUBMITTED.value,
        "status_history": [
            {
                "status": ComplaintStatus.SUBMITTED.value,
                "timestamp": utc_now(),
                "note": "Complaint submitted by citizen"
            }
        ],
        "created_at": utc_now(),
        "updated_at": utc_now()
    }
    
    result = await db.complaints.insert_one(complaint_doc)
    logger.info(f"✅ Complaint created: {complaint_id}")
    
    # Trigger AI triage
    try:
        triage_result = await triage_client.triage_complaint(complaint_doc)
        complaint_doc["triage"] = triage_result
        complaint_doc["status"] = ComplaintStatus.TRIAGED.value
        complaint_doc["status_history"].append({
            "status": ComplaintStatus.TRIAGED.value,
            "timestamp": utc_now(),
            "note": f"Auto-classified as {triage_result.get('category', 'Unknown')}"
        })
        
        # Trigger routing
        routing_result = await routing_service.route_complaint(complaint_doc)
        complaint_doc["routing"] = routing_result
        complaint_doc["status"] = ComplaintStatus.ASSIGNED.value
        complaint_doc["status_history"].append({
            "status": ComplaintStatus.ASSIGNED.value,
            "timestamp": utc_now(),
            "note": f"Assigned to {routing_result['assigned_officer_name']}"
        })
        complaint_doc["updated_at"] = utc_now()
        
        await db.complaints.update_one(
            {"_id": result.inserted_id},
            {"$set": complaint_doc}
        )
        
        logger.info(f"✅ Complaint triaged and routed: {complaint_id}")
    
    except Exception as e:
        logger.error(f"❌ Triage/Routing failed: {e}")
    
    return {
        "id": str(result.inserted_id),
        "complaint_id": complaint_id,
        "status": complaint_doc["status"]
    }

@router.get("", response_model=List[ComplaintListResponse])
async def list_complaints(
    mine: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """
    List complaints
    Citizens: only their own (mine=true enforced)
    Officers/Admins: can see all
    """
    db = await get_database()
    
    query = {}
    if current_user["role"] == "citizen" or mine:
        query["user_id"] = current_user["user_id"]
    
    complaints = await db.complaints.find(query).sort("created_at", -1).to_list(length=100)
    
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

@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get full complaint details
    Authorization: citizen (own only), officer (assigned), admin (all)
    """
    db = await get_database()
    complaint = await db.complaints.find_one({"complaint_id": complaint_id})
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Authorization check
    if current_user["role"] == "citizen":
        if complaint["user_id"] != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    elif current_user["role"] == "officer":
        if complaint.get("routing", {}).get("assigned_officer_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This complaint is not assigned to you"
            )
    
    complaint["id"] = str(complaint.pop("_id"))
    return ComplaintResponse(**complaint)
