from enum import Enum
from typing import Dict, List


class ComplaintStatus(str, Enum):
    """
    Complaint lifecycle status states
    Follows a strict workflow: SUBMITTED → TRIAGED → ASSIGNED → IN_PROGRESS → RESOLVED
    """
    SUBMITTED = "SUBMITTED"
    TRIAGED = "TRIAGED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"
    
    def __str__(self):
        return self.value


class UrgencyLevel(str, Enum):
    """
    Complaint urgency levels determined by AI triage
    """
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    
    def __str__(self):
        return self.value


class ComplaintCategory(str, Enum):
    """
    Complaint categories for classification
    Maps to different government departments
    """
    UTILITIES = "Utilities"
    WATER = "Water"
    ELECTRICITY = "Electricity"
    SANITATION = "Sanitation"
    WASTE = "Waste"
    SAFETY = "Safety"
    POLICE = "Police"
    HEALTH = "Health"
    MEDICAL = "Medical"
    EDUCATION = "Education"
    SCHOOL = "School"
    ADMINISTRATIVE = "Administrative"
    GENERAL = "General"
    
    def __str__(self):
        return self.value


# ==================== STATUS WORKFLOW RULES ====================

STATUS_TRANSITIONS: Dict[ComplaintStatus, List[ComplaintStatus]] = {
    ComplaintStatus.SUBMITTED: [
        ComplaintStatus.TRIAGED,
        ComplaintStatus.REJECTED
    ],
    ComplaintStatus.TRIAGED: [
        ComplaintStatus.ASSIGNED,
        ComplaintStatus.REJECTED
    ],
    ComplaintStatus.ASSIGNED: [
        ComplaintStatus.IN_PROGRESS,
        ComplaintStatus.REJECTED
    ],
    ComplaintStatus.IN_PROGRESS: [
        ComplaintStatus.RESOLVED,
        ComplaintStatus.REJECTED
    ],
    ComplaintStatus.RESOLVED: [],
    ComplaintStatus.REJECTED: []
}


def can_transition(current_status: str, new_status: str) -> bool:
    """
    Check if a status transition is valid according to workflow rules
    
    Args:
        current_status: Current complaint status
        new_status: Desired new status
    
    Returns:
        bool: True if transition is allowed, False otherwise
    
    Examples:
        >>> can_transition("SUBMITTED", "TRIAGED")
        True
        >>> can_transition("SUBMITTED", "RESOLVED")
        False
        >>> can_transition("IN_PROGRESS", "RESOLVED")
        True
    """
    try:
        current = ComplaintStatus(current_status)
        new = ComplaintStatus(new_status)
        
        allowed_transitions = STATUS_TRANSITIONS.get(current, [])
        return new in allowed_transitions
    
    except ValueError:
        # Invalid status value
        return False


# ==================== SLA HOURS BY URGENCY ====================

SLA_HOURS = {
    UrgencyLevel.HIGH: 6,
    UrgencyLevel.MEDIUM: 24,
    UrgencyLevel.LOW: 72
}


def get_sla_hours(urgency_level: str) -> int:
    """
    Get SLA hours for a given urgency level
    
    Args:
        urgency_level: Urgency level string (HIGH/MEDIUM/LOW)
    
    Returns:
        int: SLA hours (default: 72 for unknown urgency)
    """
    try:
        urgency = UrgencyLevel(urgency_level)
        return SLA_HOURS.get(urgency, 72)
    except ValueError:
        return 72
