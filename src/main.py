"""
Main orchestration script for the Asana Simulation Database project.

Runs the full data generation pipeline and persists results into SQLite.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from generators.organization import generate_organization
from generators.teams import generate_teams
from generators.users import generate_users
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.subtasks import generate_subtasks
from generators.comments import generate_comments
from generators.tags import generate_tags, assign_tags_to_tasks
from generators.attachments import generate_attachments
from generators.custom_fields import generate_custom_fields


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

COMPANY_NAME = os.getenv("COMPANY_NAME", "DataWhale Technologies")
TOTAL_TASKS = int(os.getenv("TOTAL_TASKS", "20000"))
DB_PATH = Path(os.getenv("DB_PATH", "output/asana_simulation.sqlite"))
SCHEMA_PATH = Path("schema.sql")


# ---------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------


def setup_database(schema_file: str | Path = SCHEMA_PATH) -> sqlite3.Connection:
    """
    Drop and recreate the SQLite database using schema.sql.

    Args:
        schema_file: Path to schema SQL file.

    Returns:
        SQLite connection.
    """
    os.makedirs(DB_PATH.parent, exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(schema_file, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    print("🗄️  Database initialized")
    return conn


def insert_data(
    conn: sqlite3.Connection,
    table_name: str,
    records: List[Dict],
) -> None:
    """
    Bulk insert records into a SQLite table.

    Args:
        conn: SQLite connection.
        table_name: Target table name.
        records: List of dictionaries representing rows.
    """
    if not records:
        print(f"⚠️  Skipped {table_name} (no records)")
        return

    columns = records[0].keys()
    placeholders = ", ".join("?" for _ in columns)
    column_clause = ", ".join(columns)

    sql = f"INSERT INTO {table_name} ({column_clause}) VALUES ({placeholders})"
    values = [tuple(record[col] for col in columns) for record in records]

    conn.executemany(sql, values)
    conn.commit()

    print(f"✅ Inserted {len(records):,} rows into {table_name}")


# ---------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------


def main() -> None:
    start_time = datetime.now()
    print("🚀 Starting Asana Simulation Data Generation\n")

    try:
        conn = setup_database()

        # --------------------------------------------------------------
        # Generate data
        # --------------------------------------------------------------

        org = generate_organization(COMPANY_NAME)
        print("[✅] Organization generated successfully.")

        teams = generate_teams(org_id=org["org_id"])
        print("[✅] Teams generated successfully.")

        users = generate_users(teams)
        print("[✅] Users generated successfully.")

        projects = generate_projects(teams)
        print("[✅] Projects generated successfully.")

        sections = generate_sections(projects)
        print("[✅] Sections generated successfully.")

        tasks = generate_tasks(projects, users, TOTAL_TASKS)
        print("[✅] Tasks generated successfully.")

        subtasks = generate_subtasks(tasks, users)
        print("[✅] Subtasks generated successfully.")

        comments = generate_comments(tasks, users)
        print("[✅] Comments generated successfully.")

        tags = generate_tags(40)
        print("[✅] Tags generated successfully.")

        task_tags = assign_tags_to_tasks(tasks, tags)
        print("[✅] Task–tag mappings generated successfully.")

        attachments = generate_attachments(tasks)
        print("[✅] Attachments generated successfully.")

        custom_fields = generate_custom_fields(projects)
        print("[✅] Custom fields generated successfully.")

        # --------------------------------------------------------------
        # Insert data (FK-safe order)
        # --------------------------------------------------------------

        insert_data(conn, "organizations", [org])
        insert_data(conn, "teams", teams)
        insert_data(conn, "users", users)
        insert_data(conn, "projects", projects)
        insert_data(conn, "sections", sections)
        insert_data(conn, "tasks", tasks)
        insert_data(conn, "subtasks", subtasks)
        insert_data(conn, "comments", comments)
        insert_data(conn, "tags", tags)
        insert_data(conn, "task_tags", task_tags)
        insert_data(conn, "attachments", attachments)
        insert_data(conn, "custom_fields", custom_fields)

        conn.close()

        # --------------------------------------------------------------
        # Summary
        # --------------------------------------------------------------

        duration = datetime.now() - start_time
        print("\n🎉 Simulation complete!")
        print(f"📦 Database ready at: {DB_PATH}")
        print(f"⏱️  Time taken: {duration}")

    except Exception as exc:
        print("❌ Simulation failed")
        print(str(exc))
        raise


if __name__ == "__main__":
    main()
