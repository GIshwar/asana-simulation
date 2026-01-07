"""
Task data generator for the Asana simulation project.

Generates realistic tasks per project with proper temporal consistency,
status/priority distributions, optional assignees, and rich text content.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import List, Dict, Optional

from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import generate_uuid, weighted_choice, random_bool
from utils.date_utils import random_date, ensure_chronology
from utils.llm_helper import generate_text, load_prompts


_PRIORITY_WEIGHTS = {
    "Low": 20,
    "Medium": 40,
    "High": 30,
    "Critical": 10,
}

_STATUS_WEIGHTS = {
    "To Do": 25,
    "In Progress": 35,
    "In Review": 20,
    "Done": 20,
}

_TECH_WORDS = [
    "authentication",
    "billing",
    "onboarding",
    "analytics",
    "dashboard",
    "notifications",
    "permissions",
    "search",
    "performance",
    "reporting",
]


def _render_prompt(template: str) -> str:
    """Replace placeholder tokens with technical words."""
    text = template
    for key in ["feature", "product", "service", "component", "functionality"]:
        text = text.replace(f"{{{key}}}", random.choice(_TECH_WORDS))
    return text


def _generate_task_name(prompts: List[str]) -> str:
    """Generate an action-oriented task name."""
    template = random.choice(prompts)
    name = _render_prompt(template)
    return name.strip().rstrip(".")


def _generate_description(project_name: str, task_name: str) -> str:
    """Generate task description via LLM with safe fallback."""
    prompt = (
        f"Write a one-sentence Asana task description for project "
        f"'{project_name}' about '{task_name}'."
    )
    try:
        return generate_text(prompt)
    except Exception:
        return f"Complete the task: {task_name}."


def generate_tasks(
    projects: List[Dict],
    users: List[Dict],
    total_task_limit: int = 40000,
) -> List[Dict]:
    """
    Generate realistic tasks across projects.
    """
    if not projects:
        raise ValueError("Projects list cannot be empty")

    random.seed(42)

    prompts_path = Path("prompts/task_prompts.txt")
    prompts = load_prompts(str(prompts_path))

    tasks: List[Dict] = []

    base_tasks_per_project = max(1, total_task_limit // max(1, len(projects)))

    # ✅ tqdm added to project loop
    for project in tqdm(projects, desc="Generating tasks (projects)"):
        project_id = project["project_id"]
        project_name = project.get("name", "Unnamed Project")

        num_tasks = random.randint(
            max(20, base_tasks_per_project // 2),
            min(150, base_tasks_per_project * 2),
        )

        # ✅ tqdm added to task loop
        for _ in tqdm(
            range(num_tasks),
            desc=f"Tasks for {project_id}",
            leave=False,
        ):
            if len(tasks) >= total_task_limit:
                print("[✅] Task generation reached total_task_limit.")
                return tasks

            task_name = _generate_task_name(prompts)
            status = weighted_choice(_STATUS_WEIGHTS)
            priority = weighted_choice(_PRIORITY_WEIGHTS)

            created_at = random_date("2021-01-01", "2025-01-01")
            due_date = random_date(created_at, "2025-12-31")

            completed_at: Optional[str] = None
            completed = status == "Done"

            if completed:
                completed_at = random_date(due_date, "2025-12-31")

            dates = ensure_chronology(
                created_at=created_at,
                due_date=due_date,
                completed_at=completed_at,
            )

            assignee_id: Optional[str] = None
            if users and random_bool(0.8):
                assignee_id = random.choice(users)["user_id"]

            tasks.append(
                {
                    "task_id": generate_uuid("task"),
                    "project_id": project_id,
                    "assignee_id": assignee_id,
                    "name": task_name,
                    "description": _generate_description(project_name, task_name),
                    "priority": priority,
                    "status": status,
                    "completed": completed,
                    "created_at": dates["created_at"],
                    "due_date": dates["due_date"],
                    "completed_at": dates["completed_at"],
                }
            )

    print(f"[✅] Generated {len(tasks):,} tasks successfully.")
    return tasks


if __name__ == "__main__":
    random.seed(42)

    fake_projects = [
        {"project_id": f"proj_{i}", "team_id": "team_1", "name": "Demo Project"}
        for i in range(3)
    ]
    fake_users = [{"user_id": f"user_{i}"} for i in range(10)]

    generated_tasks = generate_tasks(
        fake_projects,
        fake_users,
        total_task_limit=1000,
    )

    print("=== tasks generator demo ===")
    print(f"Generated {len(generated_tasks)} tasks")
    for task in generated_tasks[:3]:
        print(task)
