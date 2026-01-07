"""
Company and organization context utilities for the Asana simulation project.

Provides realistic company names, industries, and departments with optional
live scraping from Y Combinator (disabled by default).
"""

from __future__ import annotations

import random
from typing import List, Dict

import requests
from tqdm import tqdm  # ✅ ADDED

try:
    from bs4 import BeautifulSoup
except ImportError:  # BeautifulSoup is optional
    BeautifulSoup = None


# ---------------------------------------------------------------------
# Static fallback data (always available, research-inspired)
# ---------------------------------------------------------------------

_FALLBACK_COMPANIES: List[str] = [
    "ProductZen",
    "CloudForge",
    "GrowthPulse",
    "DataWhale",
    "InsightHub",
    "MetricFlow",
    "OpsPilot",
    "SecureStack",
    "DevNest",
    "PipelineLabs",
    "SignalCore",
    "LaunchPadly",
    "TeamAxis",
    "FocusLoop",
    "QuantifyIQ",
    "Workstreamer",
    "ScaleOps",
    "NimbusTech",
    "FeatureBay",
    "Sprintly",
]

_INDUSTRIES: List[str] = [
    "Analytics",
    "DevOps",
    "CRM",
    "Marketing Automation",
    "Finance",
    "Security",
    "HR Tech",
    "Collaboration",
    "AI Platforms",
    "Customer Support",
]

_DEPARTMENTS: List[str] = [
    "Engineering",
    "Design",
    "Marketing",
    "Sales",
    "Customer Success",
    "Product",
    "HR",
    "Finance",
    "Support",
    "Operations",
]


# ---------------------------------------------------------------------
# Scraping utilities
# ---------------------------------------------------------------------


def scrape_yc_companies(limit: int = 50) -> List[str]:
    """
    Attempt to scrape company names from Y Combinator's company directory.

    Args:
        limit: Maximum number of company names to return.

    Returns:
        List of company names; empty list on failure.
    """
    if BeautifulSoup is None:
        print("[WARN] BeautifulSoup not available, skipping live scrape.")
        return []

    url = "https://www.ycombinator.com/companies"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[WARN] YC scrape failed: {exc}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    names: List[str] = []

    # ✅ tqdm ADDED (this was missing)
    for tag in tqdm(
        soup.find_all("h3"),
        desc="Scraping YC companies",
    ):
        name = tag.get_text(strip=True)
        if name:
            names.append(name)
        if len(names) >= limit:
            break

    print(f"[✅] Scraped {len(names)} companies from YC.")
    return names


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def get_company_names(limit: int = 10, live: bool = False) -> List[str]:
    """
    Get a list of realistic company names.

    Args:
        limit: Number of names to return.
        live: Whether to attempt live scraping.

    Returns:
        List of company names.
    """
    if live:
        scraped = scrape_yc_companies(limit=limit)
        if scraped:
            print("[✅] Company names fetched via live scrape.")
            return scraped[:limit]

    names = random.sample(
        _FALLBACK_COMPANIES,
        k=min(limit, len(_FALLBACK_COMPANIES)),
    )
    print("[✅] Company names generated from fallback list.")
    return names


def get_industries() -> List[str]:
    """
    Return supported SaaS industry categories.

    Returns:
        List of industries.
    """
    print("[✅] Industries loaded.")
    return list(_INDUSTRIES)


def get_departments() -> List[str]:
    """
    Return realistic company departments.

    Returns:
        List of department names.
    """
    print("[✅] Departments loaded.")
    return list(_DEPARTMENTS)


def get_company_profile() -> Dict[str, str]:
    """
    Generate a random company profile.

    Returns:
        Dictionary containing company name, industry, and department.
    """
    profile = {
        "name": random.choice(_FALLBACK_COMPANIES),
        "industry": random.choice(_INDUSTRIES),
        "department": random.choice(_DEPARTMENTS),
    }
    print("[✅] Company profile generated.")
    return profile


# ---------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------

if __name__ == "__main__":
    from pprint import pprint

    random.seed(42)

    print("=== company_scraper demo ===")
    pprint(get_company_names())
    pprint(get_industries())
    pprint(get_departments())
    pprint(get_company_profile())
