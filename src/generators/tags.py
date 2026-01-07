"""
Tag data generator for the Asana simulation project.

Generates a global pool of tags and assigns them to tasks
to simulate Asana-style metadata labeling.
"""

from __future__ import annotations

import random
from typing import List, Dict

from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import generate_uuid


_COLOR_PALETTE = [
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "gray",
    "teal",
    "orange",
]

_SUGGESTED_TAG_NAMES = [
    "Backend",
    "Frontend",
    "Bug",
    "UI/UX",
    "Sprint 1",
    "Sprint 2",
    "Sprint 3",
    "Q1 Goals",
    "Q2 Goals",
    "Documentation",
    "Hotfix",
    "Urgent",
    "Testing",
    "Research",
    "Release",
    "Client Feedback",
    "Design Review",
    "Refactor",
    "API",
    "Performance",
    "Analytics",
    "Integration",
    "DevOps",
    "Security",
    "Product Launch",
    "Content",
    "SEO",
    "Infrastructure",
    "Scalability",
    "Reliability",
    "Monitoring",
    "Migration",
    "Compliance",
    "Accessibility",
    "Experiment",
    "Growth",
    "Churn Reduction",
    "User Feedback",
    "Automation",
    "Optimization",
]


def generate_tags(num_tags: int = 40) -> List[Dict]:
    """
    Generate a global pool of unique tags.

    Args:
        num_tags: Number of tags to generate.

    Returns:
        List of tag dictionaries ready for DB insertion.
    """
    if num_tags <= 0:
        raise ValueError("num_tags must be a positive integer")

    random.seed(42)

    tag_names = list(dict.fromkeys(_SUGGESTED_TAG_NAMES))
    if num_tags > len(tag_names):
        raise ValueError("num_tags exceeds available unique tag names")

    selected_names = random.sample(tag_names, k=num_tags)

    tags: List[Dict] = []

    # ✅ tqdm added (NO logic change)
    for name in tqdm(selected_names, desc="Generating tags"):
        tags.append(
            {
                "tag_id": generate_uuid("tag"),
                "name": name,
                "color": random.choice(_COLOR_PALETTE),
            }
        )

    print(f"[✅] Generated {len(tags):,} tags successfully.")
    return tags


def assign_tags_to_tasks(
    tasks: List[Dict],
    tags: List[Dict],
    max_tags_per_task: int = 3,
) -> List[Dict]:
    """
    Assign tags to tasks, creating a task-tag mapping.

    Args:
        tasks: List of task dictionaries.
        tags: List of tag dictionaries.
        max_tags_per_task: Maximum number of tags per task.

    Returns:
        List of task-tag mapping dictionaries.
    """
    if not tasks or not tags:
        return []

    if max_tags_per_task < 0:
        raise ValueError("max_tags_per_task must be non-negative")

    random.seed(42)

    task_tags: List[Dict] = []

    # ✅ tqdm added (NO logic change)
    for task in tqdm(tasks, desc="Assigning tags to tasks"):
        num_tags = random.randint(0, max_tags_per_task)
        if num_tags == 0:
            continue

        selected_tags = random.sample(
            tags,
            k=min(num_tags, len(tags)),
        )

        for tag in selected_tags:
            task_tags.append(
                {
                    "task_id": task["task_id"],
                    "tag_id": tag["tag_id"],
                }
            )

    print(f"[✅] Assigned {len(task_tags):,} task-tag pairs successfully.")
    return task_tags


if __name__ == "__main__":
    random.seed(42)

    generated_tags = generate_tags(20)
    fake_tasks = [{"task_id": f"task_{i}"} for i in range(5)]

    tagged_pairs = assign_tags_to_tasks(fake_tasks, generated_tags)

    print("=== tags generator demo ===")
    print(f"Generated {len(generated_tags)} tags")
    print(f"Assigned {len(tagged_pairs)} task-tag pairs")
    print(generated_tags[:3])
    print(tagged_pairs[:5])
