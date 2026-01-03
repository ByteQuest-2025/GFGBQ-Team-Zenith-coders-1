from ..db.mongo import get_database
from datetime import datetime, timedelta
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for generating system-wide analytics and metrics
    Used by admin dashboard
    """
    
    async def get_metrics(self) -> Dict:
        """
        Get comprehensive system metrics
        
        Returns:
            Dict: Metrics including totals, counts, averages, etc.
        """
        db = await get_database()
        
        # Total complaints
        total = await db.complaints.count_documents({})
        
        # Status counts
        status_counts = {}
        status_pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        async for doc in db.complaints.aggregate(status_pipeline):
            status_counts[doc["_id"]] = doc["count"]
        
        # Category counts
        category_counts = {}
        category_pipeline = [
            {"$group": {"_id": "$triage.category", "count": {"$sum": 1}}}
        ]
        async for doc in db.complaints.aggregate(category_pipeline):
            if doc["_id"]:  # Skip null categories
                category_counts[doc["_id"]] = doc["count"]
        
        # Urgency distribution
        urgency_distribution = {}
        urgency_pipeline = [
            {"$group": {"_id": "$triage.urgency_level", "count": {"$sum": 1}}}
        ]
        async for doc in db.complaints.aggregate(urgency_pipeline):
            if doc["_id"]:  # Skip null urgencies
                urgency_distribution[doc["_id"]] = doc["count"]
        
        # Average resolution time
        avg_resolution_hours = await self._calculate_avg_resolution_time()
        
        # Backlog size (unresolved complaints)
        backlog = await db.complaints.count_documents({
            "status": {"$in": ["SUBMITTED", "TRIAGED", "ASSIGNED", "IN_PROGRESS"]}
        })
        
        logger.info(f"📊 Analytics generated: {total} total complaints, {backlog} in backlog")
        
        return {
            "total_complaints": total,
            "status_counts": status_counts,
            "category_counts": category_counts,
            "average_resolution_hours": avg_resolution_hours,
            "backlog_size": backlog,
            "urgency_distribution": urgency_distribution
        }
    
    async def _calculate_avg_resolution_time(self) -> float:
        """
        Calculate average time to resolve complaints (in hours)
        
        Returns:
            float: Average resolution time in hours
        """
        db = await get_database()
        
        resolved_complaints = await db.complaints.find(
            {"status": "RESOLVED"}
        ).to_list(length=1000)
        
        if not resolved_complaints:
            return 0.0
        
        total_hours = 0
        count = 0
        
        for complaint in resolved_complaints:
            try:
                # Parse created timestamp
                created = datetime.fromisoformat(
                    complaint["created_at"].replace("Z", "+00:00")
                )
                
                # Find RESOLVED status in history
                resolved_entry = next(
                    (h for h in complaint.get("status_history", []) 
                     if h["status"] == "RESOLVED"),
                    None
                )
                
                if resolved_entry:
                    resolved_time = datetime.fromisoformat(
                        resolved_entry["timestamp"].replace("Z", "+00:00")
                    )
                    
                    # Calculate hours
                    hours = (resolved_time - created).total_seconds() / 3600
                    total_hours += hours
                    count += 1
            
            except Exception as e:
                logger.error(f"❌ Error calculating resolution time: {e}")
                continue
        
        if count > 0:
            avg_hours = round(total_hours / count, 2)
            logger.info(f"✅ Average resolution time: {avg_hours} hours")
            return avg_hours
        
        return 0.0
    
    async def get_officer_performance(self, officer_id: str) -> Dict:
        """
        Get performance metrics for a specific officer
        
        Args:
            officer_id: Officer user ID
        
        Returns:
            Dict: Officer performance metrics
        """
        db = await get_database()
        
        total_assigned = await db.complaints.count_documents({
            "routing.assigned_officer_id": officer_id
        })
        
        resolved = await db.complaints.count_documents({
            "routing.assigned_officer_id": officer_id,
            "status": "RESOLVED"
        })
        
        in_progress = await db.complaints.count_documents({
            "routing.assigned_officer_id": officer_id,
            "status": {"$in": ["ASSIGNED", "IN_PROGRESS"]}
        })
        
        return {
            "total_assigned": total_assigned,
            "resolved": resolved,
            "in_progress": in_progress,
            "resolution_rate": round((resolved / total_assigned * 100), 2) if total_assigned > 0 else 0.0
        }


# Create singleton instance
analytics_service = AnalyticsService()
