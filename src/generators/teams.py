"""
Team data generator for the Asana simulation project.

Generates realistic teams mapped to functional departments
within a single organization.
"""

from __future__ import annotations

import random
from typing import List, Dict

from tqdm import tqdm  # ✅ ADDED

from scrapers.company_scraper import get_departments
from utils.date_utils import random_date
from utils.random_utils import generate_uuid


_DEPARTMENT_DESCRIPTIONS = {
    "Engineering": "Responsible for building, maintaining, and scaling core product features.",
    "Design": "Handles product design, UX research, and visual branding.",
    "Marketing": "Drives growth through campaigns, content, and brand strategy.",
    "Sales": "Manages customer acquisition, partnerships, and revenue growth.",
    "Customer Success": "Ensures customer satisfaction, retention, and onboarding.",
    "Product": "Owns product strategy, roadmap, and cross-functional alignment.",
    "HR": "Manages hiring, people operations, and company culture.",
    "Finance": "Oversees budgeting, forecasting, and financial reporting.",
    "Support": "Provides technical and customer support across products.",
    "Operations": "Optimizes internal processes and business operations.",
}


def generate_teams(
    org_id: str = "org_001",
    num_teams: int = 40,
) -> List[Dict]:
    """
    Generate realistic teams for an organization.

    Args:
        org_id: Organization identifier.
        num_teams: Number of teams to generate.

    Returns:
        List of team dictionaries ready for DB insertion.
    """
    if num_teams <= 0:
        raise ValueError("num_teams must be a positive integer")

    random.seed(42)

    departments = get_departments()
    if not departments:
        raise ValueError("No departments available for team generation")

    teams: List[Dict] = []
    department_counts: Dict[str, int] = {dep: 0 for dep in departments}

    # ✅ tqdm added (NO logic change)
    for _ in tqdm(range(num_teams), desc="Generating teams"):
        department = random.choice(departments)
        department_counts[department] += 1

        team_number = department_counts[department]
        team_name = f"{department} Team {team_number}"

        description = _DEPARTMENT_DESCRIPTIONS.get(
            department,
            f"Handles core responsibilities for the {department} function.",
        )

        teams.append(
            {
                "team_id": generate_uuid("team"),
                "org_id": org_id,
                "name": team_name,
                "department": department,
                "description": description,
                "created_at": random_date(
                    "2020-01-01",
                    "2024-12-31",
                ),
            }
        )

    print(f"[✅] Generated {len(teams):,} teams successfully.")
    return teams


if __name__ == "__main__":
    random.seed(42)

    generated_teams = generate_teams(
        org_id="org_001",
        num_teams=10,
    )

    print("=== teams generator demo ===")
    print(f"Generated {len(generated_teams)} teams")
    for team in generated_teams[:3]:
        print(team)
