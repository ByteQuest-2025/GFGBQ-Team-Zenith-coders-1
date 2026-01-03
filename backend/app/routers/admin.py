from fastapi import APIRouter, Depends
from ..schemas.analytics import MetricsResponse
from ..core.deps import get_current_admin
from ..services.analytics_service import analytics_service

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/metrics", response_model=MetricsResponse)
async def get_admin_metrics(current_user: dict = Depends(get_current_admin)):
    """
    Get system-wide metrics and analytics
    Admin only
    """
    metrics = await analytics_service.get_metrics()
    return metrics
