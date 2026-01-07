"""
Subtask data generator for the Asana simulation project.

Generates realistic subtasks linked to parent tasks with
proper temporal, status, and assignment logic.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import List, Dict, Optional

from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import generate_uuid, weighted_choice, random_bool
from utils.date_utils import random_date, ensure_chronology
from utils.llm_helper import generate_text, load_prompts


_STATUS_WEIGHTS = {
    "To Do": 35,
    "In Progress": 30,
    "Done": 35,
}

_FALLBACK_SUBTASK_NAMES = [
    "Write unit tests",
    "Review PR changes",
    "Document feature behavior",
    "Deploy to staging",
    "Conduct code review",
    "Fix bug reports",
    "Prepare release notes",
    "Sync with QA",
    "Validate integration",
]


def _generate_subtask_name() -> str:
    """Generate a short, specific subtask name."""
    return random.choice(_FALLBACK_SUBTASK_NAMES)


def _generate_description(parent_name: str, subtask_name: str) -> str:
    """Generate subtask description via LLM with fallback."""
    prompt = (
        f"Write a short Asana subtask description for '{subtask_name}' "
        f"related to parent task '{parent_name}'."
    )
    try:
        return generate_text(prompt)
    except Exception:
        return f"Subtask to {subtask_name.lower()} for parent task: {parent_name}."


def generate_subtasks(
    tasks: List[Dict],
    users: List[Dict],
) -> List[Dict]:
    """
    Generate realistic subtasks for a subset of tasks.
    """
    if not tasks:
        return []

    random.seed(42)

    subtasks: List[Dict] = []

    selected_tasks = [task for task in tasks if random_bool(0.5)]

    # ✅ tqdm added to parent task loop
    for parent in tqdm(selected_tasks, desc="Generating subtasks (parent tasks)"):
        parent_status = parent.get("status", "To Do")
        parent_created = parent.get("created_at")
        parent_due = parent.get("due_date")
        parent_name = parent.get("name", "Parent Task")

        if not parent_created or not parent_due:
            continue

        max_subtasks = 2 if parent_status == "Done" else 5
        num_subtasks = random.randint(1, max_subtasks)

        # ✅ tqdm added to per-parent subtask loop
        for _ in tqdm(
            range(num_subtasks),
            desc=f"Subtasks for {parent['task_id']}",
            leave=False,
        ):
            subtask_status = (
                "Done" if parent_status == "Done" else weighted_choice(_STATUS_WEIGHTS)
            )

            created_at = random_date(parent_created, parent_due)
            due_date = random_date(created_at, parent_due)

            completed = subtask_status == "Done"
            completed_at: Optional[str] = None

            if completed:
                completed_at = random_date(created_at, due_date)

            dates = ensure_chronology(
                created_at=created_at,
                due_date=due_date,
                completed_at=completed_at,
            )

            assignee_id: Optional[str] = None
            if users and random_bool(0.8):
                assignee_id = random.choice(users)["user_id"]

            name = _generate_subtask_name()

            subtasks.append(
                {
                    "subtask_id": generate_uuid("sub"),
                    "parent_task_id": parent["task_id"],
                    "assignee_id": assignee_id,
                    "name": name,
                    "description": _generate_description(parent_name, name),
                    "status": subtask_status,
                    "completed": completed,
                    "created_at": dates["created_at"],
                    "due_date": dates["due_date"],
                    "completed_at": dates["completed_at"],
                }
            )

    print(f"[✅] Generated {len(subtasks):,} subtasks successfully.")
    return subtasks


if __name__ == "__main__":
    random.seed(42)

    fake_tasks = [
        {
            "task_id": f"task_{i}",
            "name": "Implement authentication",
            "status": "In Progress",
            "created_at": "2023-03-01",
            "due_date": "2023-04-01",
        }
        for i in range(5)
    ]

    fake_users = [{"user_id": f"user_{i}"} for i in range(3)]

    generated_subtasks = generate_subtasks(fake_tasks, fake_users)

    print("=== subtasks generator demo ===")
    print(f"Generated {len(generated_subtasks)} subtasks")
    for subtask in generated_subtasks[:3]:
        print(subtask)
