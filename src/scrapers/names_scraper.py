"""
Name, role, and email generation utilities for the Asana simulation project.

Provides realistic user identities with department-aware roles
and company-aligned email addresses.
"""

from __future__ import annotations

import random
import re
from typing import Dict, List, Optional

from faker import Faker
from tqdm import tqdm  # ✅ ADDED (non-intrusive)


# ---------------------------------------------------------------------
# Static fallback data
# ---------------------------------------------------------------------

_ROLE_MAP: Dict[str, List[str]] = {
    "Engineering": [
        "Backend Developer",
        "Frontend Developer",
        "DevOps Engineer",
        "QA Analyst",
        "Platform Engineer",
        "Mobile Developer",
    ],
    "Marketing": [
        "SEO Specialist",
        "Content Strategist",
        "Growth Analyst",
        "Marketing Manager",
        "Campaign Manager",
    ],
    "Sales": [
        "Account Executive",
        "Business Development Rep",
        "Sales Manager",
        "Sales Operations Analyst",
    ],
    "Product": [
        "Product Manager",
        "Product Designer",
        "Technical Product Manager",
        "UX Researcher",
    ],
    "HR": [
        "Recruiter",
        "HR Coordinator",
        "People Operations Manager",
        "Talent Partner",
    ],
    "Finance": [
        "Financial Analyst",
        "Accountant",
        "Finance Manager",
        "Revenue Operations Analyst",
    ],
    "Customer Success": [
        "Customer Success Manager",
        "Onboarding Specialist",
        "Support Analyst",
        "Account Manager",
    ],
    "Operations": [
        "Operations Manager",
        "Business Operations Analyst",
        "Program Manager",
    ],
}

_DOMAINS: List[str] = [".com", ".io", ".co", ".ai", ".tech"]


# ---------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------


def get_fake_name(locale: str = "en_US", gender: Optional[str] = None) -> str:
    """
    Generate a realistic full name using Faker.

    Args:
        locale: Faker locale.
        gender: Optional gender ("male" or "female").

    Returns:
        ASCII-only full name.
    """
    faker = Faker(locale)

    if gender == "male":
        name = faker.name_male()
    elif gender == "female":
        name = faker.name_female()
    else:
        name = faker.name()

    name = re.sub(r"[^\x00-\x7F]+", "", name)
    return name.strip()


def get_email_from_name(name: str, company: str) -> str:
    """
    Generate a professional email from a name and company.

    Args:
        name: Full name.
        company: Company name.

    Returns:
        Lowercase ASCII email address.
    """
    clean_name = re.sub(r"[^a-zA-Z ]", "", name).lower().strip()
    parts = clean_name.split()

    if len(parts) >= 2:
        local = f"{parts[0]}.{parts[-1]}"
    else:
        local = parts[0]

    domain = re.sub(r"[^a-zA-Z]", "", company).lower()
    tld = random.choice(_DOMAINS)

    return f"{local}@{domain}{tld}"


def get_roles(department: Optional[str] = None) -> List[str]:
    """
    Get job roles, optionally filtered by department.

    Args:
        department: Department name.

    Returns:
        List of roles.
    """
    if department and department in _ROLE_MAP:
        return list(_ROLE_MAP[department])

    roles: List[str] = []
    for values in _ROLE_MAP.values():
        roles.extend(values)

    return roles


def get_random_role(department: Optional[str] = None) -> str:
    """
    Select a random role, optionally department-scoped.

    Args:
        department: Department name.

    Returns:
        Role string.
    """
    return random.choice(get_roles(department))


def generate_user_profile(
    company: str,
    department: Optional[str] = None,
) -> Dict[str, str]:
    """
    Generate a complete synthetic user profile.

    Args:
        company: Company name.
        department: Optional department context.

    Returns:
        Dictionary with name, email, and role.
    """
    gender = random.choice(["male", "female", None])
    name = get_fake_name(gender=gender)

    return {
        "name": name,
        "email": get_email_from_name(name, company),
        "role": get_random_role(department),
    }


def get_domains() -> List[str]:
    """
    Return supported email domain extensions.

    Returns:
        List of domain strings.
    """
    return list(_DOMAINS)


# ---------------------------------------------------------------------
# Demo (ONLY place tqdm is used)
# ---------------------------------------------------------------------

if __name__ == "__main__":
    Faker.seed(42)
    random.seed(42)

    print("=== names_scraper demo ===")

    demo_profiles = [
        generate_user_profile(
            company="ProductZen",
            department="Engineering",
        )
        for _ in tqdm(range(5), desc="Generating demo user profiles")
    ]

    print("[✅] Demo user profiles generated successfully.")
    for profile in demo_profiles:
        print(profile)
