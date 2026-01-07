"""
Comment data generator for the Asana simulation project.

Generates realistic user comments for tasks, simulating collaboration,
updates, and feedback with proper temporal consistency.
"""

from __future__ import annotations

import random
from typing import List, Dict

from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import generate_uuid, random_bool
from utils.date_utils import random_date, ensure_chronology
from utils.llm_helper import generate_text


_FALLBACK_COMMENTS = [
    "Let's revisit this after the review meeting.",
    "Great progress here!",
    "Need to confirm details with the client.",
    "I’ll take this up tomorrow.",
    "Updated the spec doc for clarity.",
    "Ready for testing — please review.",
    "Merging changes now.",
    "Can someone verify the bug report?",
    "Good catch! Fixing it now.",
    "Need approval from design before proceeding.",
]


def _generate_comment_text(task_name: str) -> str:
    """Generate comment text via LLM with safe fallback."""
    prompt = (
        f"Write a short (1–2 sentence) Asana comment about the task "
        f"'{task_name}', reflecting realistic team collaboration."
    )
    try:
        return generate_text(prompt)
    except Exception:
        return random.choice(_FALLBACK_COMMENTS)


def generate_comments(
    tasks: List[Dict],
    users: List[Dict],
) -> List[Dict]:
    """
    Generate realistic comments for a subset of tasks.
    """
    if not tasks or not users:
        return []

    random.seed(42)

    comments: List[Dict] = []

    # ✅ tqdm added to task loop
    for task in tqdm(tasks, desc="Generating comments (tasks)"):
        if not random_bool(0.7):
            continue

        task_id = task["task_id"]
        task_name = task.get("name", "Task")
        created_at = task.get("created_at")
        due_date = task.get("due_date")

        if not created_at or not due_date:
            continue

        num_comments = random.randint(1, 6)

        # ✅ tqdm added to per-task comment loop
        for _ in tqdm(
            range(num_comments),
            desc=f"Comments for {task_id}",
            leave=False,
        ):
            user = random.choice(users)

            comment_created = random_date(created_at, due_date)

            dates = ensure_chronology(
                created_at=created_at,
                due_date=comment_created,
                completed_at=None,
            )

            comments.append(
                {
                    "comment_id": generate_uuid("com"),
                    "task_id": task_id,
                    "user_id": user["user_id"],
                    "text": _generate_comment_text(task_name),
                    "created_at": dates["due_date"],
                    "is_edited": random_bool(0.2),
                }
            )

    print(f"[✅] Generated {len(comments):,} comments successfully.")
    return comments


if __name__ == "__main__":
    random.seed(42)

    fake_tasks = [
        {
            "task_id": f"task_{i}",
            "name": "Implement payment flow",
            "created_at": "2023-02-01",
            "due_date": "2023-04-01",
        }
        for i in range(5)
    ]

    fake_users = [{"user_id": f"user_{i}"} for i in range(3)]

    generated_comments = generate_comments(fake_tasks, fake_users)

    print("=== comments generator demo ===")
    print(f"Generated {len(generated_comments)} comments")
    for comment in generated_comments[:3]:
        print(comment)
