"""
Custom Fields data generator for the Asana simulation project.

Generates realistic project-level custom fields that later
feed into task-level custom_field_values.
"""

from __future__ import annotations

import json
import random
from typing import List, Dict, Optional

from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import generate_uuid


_CUSTOM_FIELD_POOL = [
    {"name": "Effort Estimate", "type": "number", "possible_values": None},
    {
        "name": "Customer Segment",
        "type": "enum",
        "possible_values": ["Enterprise", "SMB", "Startup"],
    },
    {
        "name": "Priority Level",
        "type": "enum",
        "possible_values": ["Low", "Medium", "High", "Critical"],
    },
    {"name": "Confidence Score", "type": "number", "possible_values": None},
    {"name": "Sprint Number", "type": "number", "possible_values": None},
    {
        "name": "Risk Category",
        "type": "enum",
        "possible_values": ["Low", "Medium", "High"],
    },
    {"name": "Team Feedback", "type": "text", "possible_values": None},
    {
        "name": "Release Phase",
        "type": "enum",
        "possible_values": ["Alpha", "Beta", "GA"],
    },
    {
        "name": "Customer Impact",
        "type": "enum",
        "possible_values": ["Low", "Medium", "High"],
    },
    {"name": "Budget Allocation", "type": "number", "possible_values": None},
]


_TYPE_WEIGHTS = {
    "number": 40,
    "text": 30,
    "enum": 30,
}


def _weighted_type_choice() -> str:
    """Choose a custom field type using weighted distribution."""
    choices = []
    for field_type, weight in _TYPE_WEIGHTS.items():
        choices.extend([field_type] * weight)
    return random.choice(choices)


def generate_custom_fields(projects: List[Dict]) -> List[Dict]:
    """
    Generate realistic custom fields for each project.

    Args:
        projects: List of project dictionaries.

    Returns:
        List of custom field dictionaries ready for DB insertion.
    """
    if not projects:
        return []

    random.seed(42)

    custom_fields: List[Dict] = []

    # ✅ tqdm added to project loop
    for project in tqdm(projects, desc="Generating custom fields (projects)"):
        project_id = project["project_id"]

        num_fields = random.randint(2, 5)
        selected_pool = random.sample(
            _CUSTOM_FIELD_POOL,
            k=min(num_fields, len(_CUSTOM_FIELD_POOL)),
        )

        # ✅ tqdm added to per-project field loop
        for field in tqdm(
            selected_pool,
            desc=f"Custom fields for {project_id}",
            leave=False,
        ):
            field_type = field["type"]

            custom_fields.append(
                {
                    "custom_field_id": generate_uuid("cf"),
                    "project_id": project_id,
                    "name": field["name"],
                    "type": field_type,
                    "possible_values": (
                        json.dumps(field["possible_values"])
                        if field.get("possible_values") is not None
                        else None
                    ),
                }
            )

    print(f"[✅] Generated {len(custom_fields):,} custom fields successfully.")
    return custom_fields


if __name__ == "__main__":
    random.seed(42)

    fake_projects = [{"project_id": f"proj_{i}"} for i in range(3)]

    generated_fields = generate_custom_fields(fake_projects)

    print("=== custom fields generator demo ===")
    print(f"Generated {len(generated_fields)} custom fields")
    for field in generated_fields[:3]:
        print(field)
