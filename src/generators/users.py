"""
User data generator for the Asana simulation project.

Generates realistic user records with team assignment, roles,
join dates, and activity status.
"""

from __future__ import annotations

import random
from typing import List, Dict

from tqdm import tqdm  # ✅ ADDED

from scrapers.names_scraper import generate_user_profile
from scrapers.company_scraper import get_departments
from utils.date_utils import random_date
from utils.random_utils import generate_uuid, random_bool

seen_emails = set()


def generate_users(
    teams: List[Dict],
    total_users: int = 8000,
    company: str = "DataWhale",
) -> List[Dict]:
    """
    Generate realistic users distributed across teams.
    """
    if not teams:
        raise ValueError("Teams list cannot be empty")

    random.seed(42)

    users: List[Dict] = []
    seen_emails: set[str] = set()

    num_teams = len(teams)

    base_users_per_team = total_users // num_teams
    remainder = total_users % num_teams

    # ✅ tqdm added to team loop
    for idx, team in enumerate(tqdm(teams, desc="Generating users (teams)")):
        team_id = team["team_id"]
        department = team.get("department") or random.choice(get_departments())

        team_size = base_users_per_team
        if idx < remainder:
            team_size += 1

        # Add 10–20% variation in team size
        variation = int(team_size * random.uniform(-0.1, 0.2))
        team_size = max(1, team_size + variation)

        # ✅ tqdm added to per-team user loop
        for _ in tqdm(
            range(team_size),
            desc=f"Users for {team_id}",
            leave=False,
        ):
            profile = generate_user_profile(
                company=company,
                department=department,
            )

            email = profile["email"]

            # Ensure email uniqueness safely
            base_local, domain = email.split("@", 1)
            counter = 1
            unique_email = email

            while unique_email in seen_emails:
                counter += 1
                unique_email = f"{base_local}+{counter}@{domain}"

            email = unique_email
            seen_emails.add(email)

            users.append(
                {
                    "user_id": generate_uuid("user"),
                    "team_id": team_id,
                    "name": profile["name"],
                    "email": email,
                    "role": profile["role"],
                    "is_active": random_bool(0.9),
                    "joined_at": random_date(
                        "2021-01-01",
                        "2025-12-31",
                    ),
                }
            )

    random.shuffle(users)
    users = users[:total_users]

    print(f"[✅] Generated {len(users):,} users successfully.")
    return users


if __name__ == "__main__":
    random.seed(42)

    fake_teams = [
        {"team_id": f"team_{i}", "department": dep}
        for i, dep in enumerate(get_departments())
    ]

    generated_users = generate_users(
        fake_teams,
        total_users=100,
        company="DataWhale",
    )

    print("=== users generator demo ===")
    for user in generated_users[:3]:
        print(user)
