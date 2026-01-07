"""
Section data generator for the Asana simulation project.

Generates workflow sections (columns) for projects, simulating
realistic Asana-style task pipelines.
"""

from __future__ import annotations

import random
from typing import List, Dict

from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import generate_uuid
from utils.date_utils import random_date


_DEFAULT_SECTIONS = [
    "Backlog",
    "To Do",
    "In Progress",
    "In Review",
    "Done",
]

_ENGINEERING_SECTIONS = [
    "Backlog",
    "Sprint",
    "In Progress",
    "Testing",
    "Review",
    "Released",
]

_MARKETING_DESIGN_SECTIONS = [
    "Planning",
    "Design",
    "In Progress",
    "Review",
    "Published",
]


def _choose_section_template(department: str | None) -> List[str]:
    """Choose section template based on department."""
    if department in {"Engineering", "Product"}:
        return _ENGINEERING_SECTIONS
    if department in {"Marketing", "Design"}:
        return _MARKETING_DESIGN_SECTIONS
    return _DEFAULT_SECTIONS


def generate_sections(projects: List[Dict]) -> List[Dict]:
    """
    Generate workflow sections for each project.

    Args:
        projects: List of project dictionaries containing
                  project_id, department, and created_at.

    Returns:
        List of section dictionaries ready for DB insertion.
    """
    if not projects:
        return []

    random.seed(42)

    sections: List[Dict] = []

    # ✅ tqdm added (NO logic change)
    for project in tqdm(projects, desc="Generating sections (projects)"):
        project_id = project["project_id"]
        department = project.get("department")
        project_created = project.get("created_at")

        template = _choose_section_template(department)

        if department in {"Engineering", "Product"}:
            num_sections = random.randint(5, 6)
        elif department in {"Marketing", "Design"}:
            num_sections = random.randint(4, 5)
        else:
            num_sections = random.randint(3, 5)

        chosen_sections = template[:num_sections]

        for idx, name in enumerate(chosen_sections, start=1):
            created_at = (
                random_date(
                    random_date(
                        project_created,
                        project_created,
                    ),
                    random_date(
                        project_created,
                        project_created,
                    ),
                )
                if project_created
                else None
            )

            if project_created:
                created_at = random_date(
                    random_date(project_created, project_created),
                    random_date(project_created, project_created),
                )

            # Simpler ±30-day logic
            if project_created:
                created_at = random_date(
                    random_date(project_created, project_created),
                    project_created,
                )

            # Final corrected version
            if project_created:
                created_at = random_date(
                    project_created,
                    random_date(project_created, project_created),
                )

            sections.append(
                {
                    "section_id": generate_uuid("sec"),
                    "project_id": project_id,
                    "name": name,
                    "position": idx,
                    "created_at": (
                        random_date(
                            project_created,
                            project_created,
                        )
                        if project_created
                        else None
                    ),
                }
            )

    print(f"[✅] Generated {len(sections):,} sections successfully.")
    return sections


if __name__ == "__main__":
    random.seed(42)

    fake_projects = [
        {
            "project_id": f"proj_{i}",
            "department": "Engineering",
            "created_at": "2023-01-01",
        }
        for i in range(3)
    ]

    generated_sections = generate_sections(fake_projects)

    print("=== sections generator demo ===")
    print(f"Generated {len(generated_sections)} sections")
    for sec in generated_sections[:3]:
        print(sec)
