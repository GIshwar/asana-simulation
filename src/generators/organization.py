"""
Organization data generator for the Asana simulation project.

Generates a single organization record representing the company
using the simulated Asana workspace.
"""

from __future__ import annotations

import random
import re
from typing import Dict

from utils.random_utils import generate_uuid
from utils.date_utils import random_date


_INDUSTRIES = [
    "Software",
    "Software",
    "Software",
    "Marketing",
    "Finance",
    "Education",
    "Healthcare",
    "E-commerce",
]

_HEADQUARTERS = [
    "San Francisco",
    "New York",
    "London",
    "Berlin",
    "Bangalore",
    "Toronto",
    "Singapore",
]

_FALLBACK_DESCRIPTIONS = [
    "A SaaS company focused on workflow analytics and automation.",
    "A technology-driven organization building collaborative productivity tools.",
    "A modern software company enabling teams to plan, track, and execute work.",
    "A cloud-based platform helping businesses streamline operations.",
]


def _generate_domain(company_name: str) -> str:
    """Generate an email domain from a company name."""
    base = company_name.lower()
    base = re.sub(r"[^a-z0-9]", "", base)
    return f"{base}.io"


def generate_organization(
    company_name: str = "DataWhale Technologies",
) -> Dict:
    """
    Generate a single organization record.

    Args:
        company_name: Name of the organization.

    Returns:
        Organization dictionary ready for DB insertion.
    """
    random.seed(42)

    org = {
        "org_id": generate_uuid("org"),
        "name": company_name,
        "industry": random.choice(_INDUSTRIES),
        "size": random.randint(5000, 10000),
        "created_at": random_date("2015-01-01", "2020-12-31"),
        "description": random.choice(_FALLBACK_DESCRIPTIONS),
        "headquarters": random.choice(_HEADQUARTERS),
        "domain": _generate_domain(company_name),
    }

    print("[✅] Organization generated successfully.")
    return org


if __name__ == "__main__":
    random.seed(42)

    org = generate_organization("TaskNexus Inc.")

    print("=== organization generator demo ===")
    print(org)
