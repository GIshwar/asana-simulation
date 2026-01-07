"""
Utility helpers for realistic and chronologically consistent date handling
in a simulated Asana workspace.

All dates use ISO format: YYYY-MM-DD
"""

from datetime import datetime, timedelta
import random
from typing import Dict, Optional


DATE_FMT = "%Y-%m-%d"


def _to_date(date_str: str) -> datetime:
    """Convert ISO date string to datetime."""
    return datetime.strptime(date_str, DATE_FMT)


def _to_str(date_obj: datetime) -> str:
    """Convert datetime to ISO date string."""
    return date_obj.strftime(DATE_FMT)


def random_date(start: str, end: str, seed: Optional[int] = None) -> str:
    """
    Generate a random date between two ISO date strings (inclusive).

    Args:
        start: Start date in YYYY-MM-DD format.
        end: End date in YYYY-MM-DD format.
        seed: Optional seed for deterministic randomness.

    Returns:
        Random ISO date string between start and end.
    """
    if seed is not None:
        random.seed(seed)

    start_dt = _to_date(start)
    end_dt = _to_date(end)

    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    delta_days = (end_dt - start_dt).days
    offset = random.randint(0, delta_days)

    return _to_str(start_dt + timedelta(days=offset))


def add_random_offset(
    base_date: str,
    days_min: int,
    days_max: int,
    seed: Optional[int] = None,
) -> str:
    """
    Add a positive random day offset to a base date.

    Args:
        base_date: Base date in YYYY-MM-DD format.
        days_min: Minimum days to add (inclusive).
        days_max: Maximum days to add (inclusive).
        seed: Optional seed for deterministic randomness.

    Returns:
        New ISO date string after offset.
    """
    if days_min < 0 or days_max < days_min:
        raise ValueError("Invalid day offset range")

    if seed is not None:
        random.seed(seed)

    base_dt = _to_date(base_date)
    offset_days = random.randint(days_min, days_max)

    return _to_str(base_dt + timedelta(days=offset_days))


def ensure_chronology(
    created_at: str,
    due_date: Optional[str] = None,
    completed_at: Optional[str] = None,
) -> Dict[str, Optional[str]]:
    """
    Ensure chronological consistency between created, due, and completed dates.

    Rules enforced:
    - due_date >= created_at
    - completed_at >= due_date (if due_date exists)
    - completed_at >= created_at (fallback)

    Inconsistent dates are auto-corrected by adding 1–7 days.

    Args:
        created_at: Creation date (YYYY-MM-DD).
        due_date: Optional due date.
        completed_at: Optional completion date.

    Returns:
        Dictionary with corrected dates.
    """
    created_dt = _to_date(created_at)

    due_dt = _to_date(due_date) if due_date else None
    completed_dt = _to_date(completed_at) if completed_at else None

    if due_dt and due_dt < created_dt:
        due_dt = created_dt + timedelta(days=random.randint(1, 7))

    if completed_dt:
        reference_dt = due_dt if due_dt else created_dt
        if completed_dt < reference_dt:
            completed_dt = reference_dt + timedelta(days=random.randint(1, 7))

    return {
        "created_at": _to_str(created_dt),
        "due_date": _to_str(due_dt) if due_dt else None,
        "completed_at": _to_str(completed_dt) if completed_dt else None,
    }


if __name__ == "__main__":
    print("=== date_utils demo ===")

    created = random_date("2023-01-01", "2023-06-01", seed=42)
    due = add_random_offset(created, 5, 20, seed=42)
    completed = add_random_offset(due, 1, 7, seed=42)

    print(
        ensure_chronology(
            created_at=created,
            due_date=due,
            completed_at=completed,
        )
    )

    # ✅ ADDED (this was the missing part)
    print("[✅] date_utils executed successfully.")
