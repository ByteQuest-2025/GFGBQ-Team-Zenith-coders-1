# This file makes the routers directory a Python package
from .auth import router as auth
from .complaints import router as complaints
from .officers import router as officer
from .admin import router as admin

__all__ = ["auth", "complaints", "officer", "admin"]
