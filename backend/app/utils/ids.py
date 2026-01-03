import random
import string
from datetime import datetime


def generate_user_id() -> str:
    """
    Generate unique user ID in format: USR_XXXXXX
    
    Returns:
        str: User ID (e.g., "USR_A3B9K2")
    
    Examples:
        >>> generate_user_id()
        'USR_K8M2N5'
    """
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"USR_{random_suffix}"


def generate_complaint_id() -> str:
    """
    Generate unique complaint ID in format: COMP-YYYY-XXXXXX
    
    Returns:
        str: Complaint ID (e.g., "COMP-2026-123456")
    
    Examples:
        >>> generate_complaint_id()
        'COMP-2026-845721'
    """
    year = datetime.utcnow().year
    random_num = random.randint(100000, 999999)
    return f"COMP-{year}-{random_num:06d}"


def generate_department_id(name: str) -> str:
    """
    Generate department ID from department name
    Takes first letter of each word (up to 3 words)
    
    Args:
        name: Department name (e.g., "Utilities Department")
    
    Returns:
        str: Department ID (e.g., "DEPT_UD")
    
    Examples:
        >>> generate_department_id("Utilities Department")
        'DEPT_UD'
        >>> generate_department_id("Municipal Sanitation Services")
        'DEPT_MSS'
    """
    # Extract first letter of each word (max 3 words)
    words = name.split()[:3]
    prefix = ''.join([word[0].upper() for word in words])
    return f"DEPT_{prefix}"


def generate_officer_badge() -> str:
    """
    Generate officer badge number in format: OFF-XXXX
    
    Returns:
        str: Badge number (e.g., "OFF-8472")
    
    Examples:
        >>> generate_officer_badge()
        'OFF-3829'
    """
    badge_num = random.randint(1000, 9999)
    return f"OFF-{badge_num}"


def generate_tracking_number() -> str:
    """
    Generate tracking number for complaint updates
    Format: TRK-YYYYMMDD-XXXXX
    
    Returns:
        str: Tracking number (e.g., "TRK-20260103-48572")
    
    Examples:
        >>> generate_tracking_number()
        'TRK-20260103-72849'
    """
    date_str = datetime.utcnow().strftime("%Y%m%d")
    random_num = random.randint(10000, 99999)
    return f"TRK-{date_str}-{random_num}"


def validate_complaint_id(complaint_id: str) -> bool:
    """
    Validate complaint ID format
    
    Args:
        complaint_id: Complaint ID to validate
    
    Returns:
        bool: True if valid format
    
    Examples:
        >>> validate_complaint_id("COMP-2026-123456")
        True
        >>> validate_complaint_id("invalid")
        False
    """
    import re
    pattern = r'^COMP-\d{4}-\d{6}$'
    return bool(re.match(pattern, complaint_id))


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format
    
    Args:
        user_id: User ID to validate
    
    Returns:
        bool: True if valid format
    
    Examples:
        >>> validate_user_id("USR_A3B9K2")
        True
        >>> validate_user_id("invalid")
        False
    """
    import re
    pattern = r'^USR_[A-Z0-9]{6}$'
    return bool(re.match(pattern, user_id))
