import logging
from typing import Dict, Optional
from ..db.mongo import get_database
from ..models.complaint import ComplaintCategory, UrgencyLevel, get_sla_hours
from ..models.department import get_department_for_category

logger = logging.getLogger(__name__)


class RoutingService:
    """
    Service for intelligent complaint routing
    Assigns complaints to appropriate departments and officers
    """
    
    async def route_complaint(self, complaint: dict) -> dict:
        """
        Route complaint to appropriate department and officer
        
        Args:
            complaint: Complaint document with triage results
        
        Returns:
            dict: Routing data with assigned department, officer, and SLA
        """
        category = complaint.get("triage", {}).get("category", "Administrative")
        urgency = complaint.get("triage", {}).get("urgency_level", "LOW")
        location = complaint.get("location", {})
        
        # Get department based on category
        department_id = get_department_for_category(category)
        
        # Assign officer (load-balanced)
        officer = await self._assign_officer(department_id, urgency, location)
        
        # Calculate SLA hours
        sla_hours = get_sla_hours(urgency)
        
        # Determine if escalation is needed
        needs_escalation = urgency == "HIGH"
        
        routing_data = {
            "assigned_department": department_id,
            "assigned_officer_id": officer["user_id"],
            "assigned_officer_name": officer["name"],
            "sla_hours": sla_hours,
            "escalation": {
                "needed": needs_escalation,
                "level": "L1" if needs_escalation else None
            }
        }
        
        logger.info(f"✅ Routed to {department_id} → {officer['name']} (SLA: {sla_hours}h)")
        return routing_data
    
    async def _assign_officer(self, department_id: str, urgency: str, location: dict) -> dict:
        """
        Assign officer based on department, workload, and location
        
        Args:
            department_id: Target department ID
            urgency: Complaint urgency level
            location: Complaint location data
        
        Returns:
            dict: Officer document with user_id and name
        """
        db = await get_database()
        
        # Try to find officer in the specific department
        officer = await db.users.find_one({
            "role": "officer",
            "department_id": department_id
        })
        
        if officer:
            logger.info(f"✅ Assigned to department officer: {officer['name']}")
            return officer
        
        # Fallback: Find any available officer
        officer = await db.users.find_one({"role": "officer"})
        
        if officer:
            logger.warning(f"⚠️ No officer in {department_id}, assigned to: {officer['name']}")
            return officer
        
        # Last resort: Create a fallback admin officer
        logger.warning("⚠️ No officers found, using admin fallback")
        return {
            "user_id": "USR_ADMIN",
            "name": "Admin Officer",
            "role": "officer"
        }
    
    async def reassign_complaint(
        self, 
        complaint_id: str, 
        new_officer_id: str
    ) -> bool:
        """
        Reassign complaint to a different officer
        
        Args:
            complaint_id: Complaint ID to reassign
            new_officer_id: Target officer user ID
        
        Returns:
            bool: True if reassignment successful
        """
        db = await get_database()
        
        # Get new officer details
        officer = await db.users.find_one({"user_id": new_officer_id, "role": "officer"})
        
        if not officer:
            logger.error(f"❌ Officer not found: {new_officer_id}")
            return False
        
        # Update complaint routing
        result = await db.complaints.update_one(
            {"complaint_id": complaint_id},
            {
                "$set": {
                    "routing.assigned_officer_id": officer["user_id"],
                    "routing.assigned_officer_name": officer["name"]
                }
            }
        )
        
        if result.modified_count > 0:
            logger.info(f"✅ Complaint {complaint_id} reassigned to {officer['name']}")
            return True
        
        return False


# Create singleton instance
routing_service = RoutingService()
