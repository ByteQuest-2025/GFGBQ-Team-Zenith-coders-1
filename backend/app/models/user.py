from enum import Enum


class UserRole(str, Enum):
    """
    User roles in the grievance redressal system
    """
    CITIZEN = "citizen"
    OFFICER = "officer"
    ADMIN = "admin"
    
    def __str__(self):
        return self.value
