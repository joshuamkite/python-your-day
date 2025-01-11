from datetime import datetime


def validate_date(date_str: str) -> datetime:
    """Validate date string and return datetime object."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.year < 1754:
            raise ValueError("Date must be after 1754 (Gregorian calendar adoption)")
        return date
    except ValueError as e:
        raise ValueError(f"Invalid date format. Please use YYYY-MM-DD format: {e}")
