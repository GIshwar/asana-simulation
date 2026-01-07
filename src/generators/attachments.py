"""
Attachment data generator for the Asana simulation project.

Generates realistic file attachments for tasks, simulating
documents, screenshots, reports, and other common artifacts.
"""

from __future__ import annotations

import random
import re
from typing import List, Dict

from tqdm import tqdm  # ✅ ADDED

from utils.random_utils import generate_uuid
from utils.date_utils import random_date


_FILE_TYPE_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".pdf": "application/pdf",
    ".csv": "text/csv",
    ".xlsx": "application/vnd.ms-excel",
    ".zip": "application/zip",
    ".pptx": "application/vnd.ms-powerpoint",
}

_FILE_NAME_SUFFIXES = [
    "v1",
    "v2",
    "v3",
    "final",
    "draft",
    "review",
]

_AVG_SIZE_RANGE_KB = (500, 2500)
_MAX_SIZE_RANGE_KB = (50, 5000)


def _sanitize_name(name: str) -> str:
    """Convert task name into a filesystem-friendly base name."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def _generate_file_name(task_name: str) -> str:
    """Generate a realistic file name derived from task name."""
    base = _sanitize_name(task_name)
    suffix = random.choice(_FILE_NAME_SUFFIXES)
    ext = random.choice(list(_FILE_TYPE_MAP.keys()))
    return f"{base}_{suffix}{ext}"


def generate_attachments(tasks: List[Dict]) -> List[Dict]:
    """
    Generate realistic attachments for a subset of tasks.
    """
    if not tasks:
        return []

    random.seed(42)

    attachments: List[Dict] = []

    # ✅ tqdm added to task loop
    for task in tqdm(tasks, desc="Generating attachments (tasks)"):
        if random.random() > 0.5:
            continue

        task_id = task["task_id"]
        task_name = task.get("name", "task")
        created_at = task.get("created_at")
        due_date = task.get("due_date")

        if not created_at or not due_date:
            continue

        num_attachments = random.randint(1, 3)
        used_names = set()

        # ✅ tqdm added to per-task attachment loop
        for _ in tqdm(
            range(num_attachments),
            desc=f"Attachments for {task_id}",
            leave=False,
        ):
            file_name = _generate_file_name(task_name)
            while file_name in used_names:
                file_name = _generate_file_name(task_name)
            used_names.add(file_name)

            ext = "." + file_name.split(".")[-1]
            mime_type = _FILE_TYPE_MAP.get(ext, "application/octet-stream")

            file_size_kb = random.randint(*_AVG_SIZE_RANGE_KB)
            if random.random() < 0.15:
                file_size_kb = random.randint(*_MAX_SIZE_RANGE_KB)

            uploaded_at = random_date(created_at, due_date)

            attachments.append(
                {
                    "attachment_id": generate_uuid("att"),
                    "task_id": task_id,
                    "file_name": file_name,
                    "file_type": mime_type,
                    "file_size_kb": file_size_kb,
                    "uploaded_at": uploaded_at,
                    "url": f"https://example.com/files/{file_name}",
                }
            )

    print(f"[✅] Generated {len(attachments):,} attachments successfully.")
    return attachments


if __name__ == "__main__":
    random.seed(42)

    fake_tasks = [
        {
            "task_id": f"task_{i}",
            "name": f"Design API Spec {i}",
            "created_at": "2023-01-01",
            "due_date": "2023-03-01",
        }
        for i in range(5)
    ]

    generated_attachments = generate_attachments(fake_tasks)

    print("=== attachments generator demo ===")
    print(f"Generated {len(generated_attachments)} attachments")
    for att in generated_attachments[:3]:
        print(att)
