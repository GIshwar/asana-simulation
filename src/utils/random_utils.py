"""
Randomness and UUID utilities for the Asana simulation project.

Centralizes all random behavior to ensure consistency and reproducibility
across generators.
"""

from __future__ import annotations

import random
import uuid
import string
from typing import Dict

from tqdm import tqdm  # ✅ ADDED


_SAMPLE_VERBS = [
    "optimize",
    "review",
    "implement",
    "design",
    "analyze",
    "improve",
    "refactor",
    "validate",
    "coordinate",
]

_SAMPLE_ADJECTIVES = [
    "scalable",
    "robust",
    "efficient",
    "strategic",
    "critical",
    "enterprise",
    "automated",
    "modular",
]

_SAMPLE_NOUNS = [
    "workflow",
    "pipeline",
    "feature",
    "dashboard",
    "integration",
    "onboarding flow",
    "API",
    "deployment",
    "report",
    "system",
]


def set_seed(seed: int) -> None:
    """Globally set the random seed for reproducibility."""
    random.seed(seed)


def generate_uuid(prefix: str | None = None) -> str:
    """
    Generate a UUID4 string, optionally prefixed.

    Args:
        prefix: Optional prefix (e.g., 'user', 'task').

    Returns:
        UUID string, optionally prefixed.
    """
    uid = str(uuid.uuid4())
    return f"{prefix}_{uid}" if prefix else uid


def weighted_choice(choices: Dict[str, int]) -> str:
    """
    Perform a weighted random selection.

    Args:
        choices: Mapping of item -> weight.

    Returns:
        Selected item based on weights.
    """
    if not choices:
        raise ValueError("Choices dictionary cannot be empty")

    items = list(choices.keys())
    weights = list(choices.values())

    return random.choices(items, weights=weights, k=1)[0]


def random_bool(probability_true: float = 0.5) -> bool:
    """
    Return True with the given probability.

    Args:
        probability_true: Probability of returning True (0.0–1.0).

    Returns:
        Boolean result.
    """
    if not 0.0 <= probability_true <= 1.0:
        raise ValueError("probability_true must be between 0.0 and 1.0")

    return random.random() < probability_true


def random_sentence(words_min: int = 5, words_max: int = 12) -> str:
    """
    Generate a randomly structured sentence.

    Used for comments, short descriptions, tags, etc.

    Args:
        words_min: Minimum number of words.
        words_max: Maximum number of words.

    Returns:
        Capitalized sentence ending with a period.
    """
    if words_min <= 0 or words_max < words_min:
        raise ValueError("Invalid word count range")

    verb = random.choice(_SAMPLE_VERBS)
    adjective = random.choice(_SAMPLE_ADJECTIVES)
    noun = random.choice(_SAMPLE_NOUNS)

    core_phrase = f"{verb} {adjective} {noun}"

    remaining_words = random.randint(
        max(0, words_min - len(core_phrase.split())),
        max(0, words_max - len(core_phrase.split())),
    )

    filler = random.choices(
        list(string.ascii_lowercase),
        k=remaining_words,
    )

    sentence = " ".join([core_phrase] + filler).capitalize()
    return f"{sentence}."


if __name__ == "__main__":
    set_seed(42)

    print("=== random_utils demo ===")

    demo_steps = [
        "Generate UUID",
        "Weighted choice",
        "Random boolean",
        "Random sentence",
    ]

    for step in tqdm(demo_steps, desc="Running random_utils demo"):  # ✅ ADDED
        if step == "Generate UUID":
            generate_uuid("task")
        elif step == "Weighted choice":
            weighted_choice({"Done": 60, "In Progress": 30, "Stuck": 10})
        elif step == "Random boolean":
            random_bool(0.7)
        elif step == "Random sentence":
            random_sentence()

    print("[✅] random_utils demo completed successfully.")  # ✅ ADDED
