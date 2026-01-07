"""
Project data generator for the Asana simulation project.

Generates realistic projects per team with valid timelines,
statuses, and SaaS-relevant names and descriptions.
"""

from __future__ import annotations

import random
from typing import List, Dict

from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import generate_uuid, weighted_choice
from utils.date_utils import random_date, ensure_chronology
from utils.llm_helper import generate_text
from scrapers.company_scraper import get_departments


_PROJECT_NAMES = [
    "Growth Analytics Platform",
    "Mobile Redesign Sprint",
    "Customer Portal",
    "Onboarding Revamp",
    "Marketing Automation Integration",
    "Internal API Gateway",
    "Security Audit 2024",
    "Employee Experience Dashboard",
    "Performance Reporting Tool",
    "Cloud Cost Optimizer",
]


_STATUS_WEIGHTS = {
    "Active": 60,
    "Completed": 25,
    "On Hold": 10,
    "Not Started": 5,
}


_FALLBACK_DESCRIPTIONS = [
    "Build a scalable internal solution aligned with business objectives.",
    "Improve system reliability and user experience across teams.",
    "Deliver a cross-functional initiative supporting company growth.",
    "Modernize workflows and infrastructure for long-term scalability.",
]


def _generate_description(project_name: str, department: str) -> str:
    """Generate a project description using LLM or fallback text."""
    prompt = (
        f"Write a concise project description for a {department} project "
        f"named '{project_name}' in a B2B SaaS company."
    )
    try:
        return generate_text(prompt)
    except Exception:
        return random.choice(_FALLBACK_DESCRIPTIONS)


def generate_projects(
    teams: List[Dict],
    company_name: str = "DataWhale",
) -> List[Dict]:
    """
    Generate realistic projects for each team.
    """
    if not teams:
        raise ValueError("Teams list cannot be empty")

    random.seed(42)

    projects: List[Dict] = []

    # ✅ tqdm added to team loop
    for team in tqdm(teams, desc="Generating projects (teams)"):
        team_id = team["team_id"]
        department = team.get("department") or random.choice(get_departments())

        num_projects = random.randint(3, 12)

        # ✅ tqdm added to per-team project loop
        for _ in tqdm(
            range(num_projects),
            desc=f"Projects for {team_id}",
            leave=False,
        ):
            project_name = random.choice(_PROJECT_NAMES)
            status = weighted_choice(_STATUS_WEIGHTS)

            created_at = random_date("2021-01-01", "2025-01-01")

            start_date = random_date(
                created_at,
                "2025-06-30",
            )

            end_date = None
            if status in {"Completed", "Active"}:
                end_date = random_date(start_date, "2025-12-31")

            dates = ensure_chronology(
                created_at=created_at,
                due_date=end_date,
                completed_at=None,
            )

            projects.append(
                {
                    "project_id": generate_uuid("proj"),
                    "team_id": team_id,
                    "department": department,
                    "name": project_name,
                    "description": _generate_description(
                        project_name,
                        department,
                    ),
                    "status": status,
                    "start_date": start_date,
                    "end_date": dates["due_date"],
                    "created_at": created_at,
                }
            )

    print(f"[✅] Generated {len(projects):,} projects successfully.")
    return projects


if __name__ == "__main__":
    random.seed(42)

    fake_teams = [
        {"team_id": f"team_{i}", "department": "Engineering"} for i in range(3)
    ]

    generated_projects = generate_projects(fake_teams)

    print("=== projects generator demo ===")
    print(f"Generated {len(generated_projects)} projects.")
    for project in generated_projects[:3]:
        print(project)
