from enum import Enum
from typing import Dict, List


class DepartmentType(str, Enum):
    """
    Government department types
    """
    UTILITIES = "DEPT_UTIL"
    MUNICIPAL = "DEPT_MUN"
    POLICE = "DEPT_POL"
    HEALTH = "DEPT_HLT"
    EDUCATION = "DEPT_EDU"
    ADMINISTRATION = "DEPT_ADM"
    
    def __str__(self):
        return self.value


# ==================== CATEGORY TO DEPARTMENT MAPPING ====================

CATEGORY_DEPARTMENT_MAP: Dict[str, str] = {
    # Utilities
    "Utilities": "DEPT_UTIL",
    "Water": "DEPT_UTIL",
    "Electricity": "DEPT_UTIL",
    
    # Municipal
    "Sanitation": "DEPT_MUN",
    "Waste": "DEPT_MUN",
    
    # Safety
    "Safety": "DEPT_POL",
    "Police": "DEPT_POL",
    
    # Health
    "Health": "DEPT_HLT",
    "Medical": "DEPT_HLT",
    
    # Education
    "Education": "DEPT_EDU",
    "School": "DEPT_EDU",
    
    # Administrative
    "Administrative": "DEPT_ADM",
    "General": "DEPT_ADM"
}


def get_department_for_category(category: str) -> str:
    """
    Get department ID for a given complaint category
    
    Args:
        category: Complaint category
    
    Returns:
        str: Department ID (defaults to DEPT_ADM if not found)
    """
    return CATEGORY_DEPARTMENT_MAP.get(category, "DEPT_ADM")


# ==================== DEPARTMENT METADATA ====================

DEPARTMENT_INFO: Dict[str, Dict] = {
    "DEPT_UTIL": {
        "name": "Utilities Department",
        "categories": ["Utilities", "Water", "Electricity"],
        "description": "Handles water supply, electricity, and utility services"
    },
    "DEPT_MUN": {
        "name": "Municipal Department",
        "categories": ["Sanitation", "Waste"],
        "description": "Manages sanitation, waste collection, and public cleanliness"
    },
    "DEPT_POL": {
        "name": "Police Department",
        "categories": ["Safety", "Police"],
        "description": "Handles public safety and law enforcement issues"
    },
    "DEPT_HLT": {
        "name": "Health Department",
        "categories": ["Health", "Medical"],
        "description": "Manages healthcare facilities and medical emergencies"
    },
    "DEPT_EDU": {
        "name": "Education Department",
        "categories": ["Education", "School"],
        "description": "Oversees schools and educational institutions"
    },
    "DEPT_ADM": {
        "name": "Administrative Department",
        "categories": ["Administrative", "General"],
        "description": "Handles general administrative and miscellaneous complaints"
    }
}
