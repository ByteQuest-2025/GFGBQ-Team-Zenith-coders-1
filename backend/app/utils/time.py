from datetime import datetime, timezone, timedelta
from typing import Optional


def utc_now() -> str:
    """
    Get current UTC timestamp in ISO 8601 format
    
    Returns:
        str: ISO 8601 timestamp (e.g., "2026-01-03T10:30:00+00:00")
    
    Examples:
        >>> utc_now()
        '2026-01-03T10:30:00+00:00'
    """
    return datetime.now(timezone.utc).isoformat()


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime object to ISO 8601 string
    
    Args:
        dt: Datetime object to format
    
    Returns:
        str: ISO 8601 timestamp string
    
    Examples:
        >>> dt = datetime(2026, 1, 3, 10, 30, 0)
        >>> format_timestamp(dt)
        '2026-01-03T10:30:00+00:00'
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse ISO 8601 timestamp string to datetime object
    
    Args:
        timestamp_str: ISO 8601 timestamp string
    
    Returns:
        datetime: Datetime object with timezone
    
    Examples:
        >>> parse_timestamp("2026-01-03T10:30:00+00:00")
        datetime.datetime(2026, 1, 3, 10, 30, tzinfo=datetime.timezone.utc)
    """
    # Handle both with and without 'Z' suffix
    clean_str = timestamp_str.replace("Z", "+00:00")
    return datetime.fromisoformat(clean_str)


def calculate_sla_deadline(created_at: str, sla_hours: int) -> str:
    """
    Calculate SLA deadline based on creation time and SLA hours
    
    Args:
        created_at: Creation timestamp (ISO 8601)
        sla_hours: SLA hours to add
    
    Returns:
        str: Deadline timestamp (ISO 8601)
    
    Examples:
        >>> calculate_sla_deadline("2026-01-03T10:00:00+00:00", 24)
        '2026-01-04T10:00:00+00:00'
    """
    created = parse_timestamp(created_at)
    deadline = created + timedelta(hours=sla_hours)
    return format_timestamp(deadline)


def is_sla_breached(created_at: str, sla_hours: int, current_time: Optional[str] = None) -> bool:
    """
    Check if SLA has been breached
    
    Args:
        created_at: Creation timestamp (ISO 8601)
        sla_hours: SLA hours
        current_time: Optional current time (defaults to now)
    
    Returns:
        bool: True if SLA breached
    
    Examples:
        >>> is_sla_breached("2026-01-01T10:00:00+00:00", 24, "2026-01-03T10:00:00+00:00")
        True
    """
    deadline = parse_timestamp(calculate_sla_deadline(created_at, sla_hours))
    now = parse_timestamp(current_time) if current_time else datetime.now(timezone.utc)
    return now > deadline


def get_hours_elapsed(start_time: str, end_time: Optional[str] = None) -> float:
    """
    Calculate hours elapsed between two timestamps
    
    Args:
        start_time: Start timestamp (ISO 8601)
        end_time: End timestamp (defaults to now)
    
    Returns:
        float: Hours elapsed
    
    Examples:
        >>> get_hours_elapsed("2026-01-03T10:00:00+00:00", "2026-01-03T14:30:00+00:00")
        4.5
    """
    start = parse_timestamp(start_time)
    end = parse_timestamp(end_time) if end_time else datetime.now(timezone.utc)
    delta = end - start
    return delta.total_seconds() / 3600


def get_time_remaining(created_at: str, sla_hours: int) -> float:
    """
    Get remaining hours until SLA deadline
    
    Args:
        created_at: Creation timestamp (ISO 8601)
        sla_hours: SLA hours
    
    Returns:
        float: Remaining hours (negative if breached)
    
    Examples:
        >>> get_time_remaining("2026-01-03T10:00:00+00:00", 24)
        20.5
    """
    deadline = parse_timestamp(calculate_sla_deadline(created_at, sla_hours))
    now = datetime.now(timezone.utc)
    delta = deadline - now
    return delta.total_seconds() / 3600


def format_duration(hours: float) -> str:
    """
    Format hours as human-readable duration
    
    Args:
        hours: Number of hours
    
    Returns:
        str: Formatted duration string
    
    Examples:
        >>> format_duration(48.5)
        '2 days 30 minutes'
        >>> format_duration(1.5)
        '1 hour 30 minutes'
    """
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} minutes"
    elif hours < 24:
        full_hours = int(hours)
        minutes = int((hours - full_hours) * 60)
        if minutes > 0:
            return f"{full_hours} {'hour' if full_hours == 1 else 'hours'} {minutes} minutes"
        return f"{full_hours} {'hour' if full_hours == 1 else 'hours'}"
    else:
        days = int(hours / 24)
        remaining_hours = int(hours % 24)
        if remaining_hours > 0:
            return f"{days} {'day' if days == 1 else 'days'} {remaining_hours} {'hour' if remaining_hours == 1 else 'hours'}"
        return f"{days} {'day' if days == 1 else 'days'}"


def get_date_range(days: int = 7) -> tuple:
    """
    Get start and end timestamps for a date range
    
    Args:
        days: Number of days in the range (default: 7)
    
    Returns:
        tuple: (start_timestamp, end_timestamp) in ISO 8601 format
    
    Examples:
        >>> get_date_range(7)
        ('2025-12-27T10:00:00+00:00', '2026-01-03T10:00:00+00:00')
    """
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    return (format_timestamp(start), format_timestamp(end))
