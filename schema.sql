-- ===========================================================
-- ASANA SIMULATION DATABASE SCHEMA
-- Author: GIshwar
-- Description: Fully normalized and realistic schema
-- Entities: 11 core + 2 relationship = 13 total tables
-- ===========================================================

-- ===========================================================
-- 1. ORGANIZATIONS
-- ===========================================================
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT, -- e.g., "asana.io"
    created_at DATE DEFAULT CURRENT_DATE
);

-- ===========================================================
-- 2. TEAMS
-- ===========================================================
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- ===========================================================
-- 3. USERS
-- ===========================================================
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT CHECK(role IN ('Manager', 'Developer', 'Designer', 'QA', 'Analyst', 'Intern')),
    is_active BOOLEAN DEFAULT 1,
    joined_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- ===========================================================
-- 4. PROJECTS
-- ===========================================================
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status TEXT CHECK(status IN ('Not Started', 'Active', 'Completed', 'On Hold')),
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- ===========================================================
-- 5. SECTIONS
-- ===========================================================
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- ===========================================================
-- 6. TASKS
-- ===========================================================
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    priority TEXT CHECK(priority IN ('Low', 'Medium', 'High', 'Critical')),
    status TEXT CHECK(status IN ('To Do', 'In Progress', 'In Review', 'Done')),
    due_date DATE,
    created_at DATE DEFAULT CURRENT_DATE,
    completed BOOLEAN DEFAULT 0,
    estimated_hours REAL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

-- ===========================================================
-- 7. SUBTASKS
-- ===========================================================
CREATE TABLE subtasks (
    subtask_id TEXT PRIMARY KEY,
    parent_task_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    status TEXT CHECK(status IN ('To Do', 'In Progress', 'Done')),
    created_at DATE DEFAULT CURRENT_DATE,
    completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

-- ===========================================================
-- 8. COMMENTS
-- ===========================================================
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE,
    is_edited BOOLEAN DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ===========================================================
-- 9. TAGS
-- ===========================================================
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    color TEXT CHECK(color IN ('red', 'blue', 'green', 'yellow', 'purple', 'gray'))
);

-- ===========================================================
-- 10. TASK_TAGS (Many-to-Many Link)
-- ===========================================================
CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- ===========================================================
-- 11. CUSTOM_FIELDS
-- ===========================================================
CREATE TABLE custom_fields (
    field_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    field_type TEXT CHECK(field_type IN ('text', 'numeric', 'date', 'boolean'))
);

-- ===========================================================
-- 12. CUSTOM_FIELD_VALUES (Many-to-Many Link)
-- ===========================================================
CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    value TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_fields(field_id)
);

-- ===========================================================
-- 13. ATTACHMENTS
-- ===========================================================
CREATE TABLE attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT,
    file_name TEXT NOT NULL,
    file_type TEXT CHECK(file_type IN ('pdf', 'png', 'jpg', 'jpeg', 'docx', 'xlsx', 'csv')),
    uploaded_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
