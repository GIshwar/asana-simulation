PRAGMA foreign_keys = ON;

-- ===========================================================
-- ASANA SIMULATION DATABASE SCHEMA (FINAL, GENERATOR-ALIGNED)
-- Author: GIshwar
-- ===========================================================


-- ===========================================================
-- 1. ORGANIZATIONS
-- ===========================================================
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT,
    industry TEXT,
    size INTEGER,
    description TEXT,
    headquarters TEXT,
    created_at DATE DEFAULT CURRENT_DATE
);


-- ===========================================================
-- 2. TEAMS
-- ===========================================================
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    department TEXT,
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
    role TEXT,
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
    department TEXT NOT NULL,        -- ✅ ADD THIS
    status TEXT,
    start_date DATE,
    end_date DATE,
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
    position INTEGER NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);


-- ===========================================================
-- 6. TASKS
-- ===========================================================
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT,
    assignee_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    priority TEXT,
    status TEXT,
    completed BOOLEAN DEFAULT 0,
    created_at DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    completed_at DATE,
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
    assignee_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT,
    completed BOOLEAN DEFAULT 0,
    created_at DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    completed_at DATE,
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
    color TEXT
);


-- ===========================================================
-- 10. TASK_TAGS (Many-to-Many)
-- ===========================================================
CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);


-- ===========================================================
-- 11. ATTACHMENTS
-- ===========================================================
CREATE TABLE attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT,
    file_size_kb INTEGER,
    uploaded_at DATE DEFAULT CURRENT_DATE,
    url TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);


-- ===========================================================
-- 12. CUSTOM_FIELDS
-- ===========================================================
CREATE TABLE custom_fields (
    custom_field_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT CHECK(type IN ('text', 'number', 'enum')),
    possible_values TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);


-- ===========================================================
-- 13. CUSTOM_FIELD_VALUES
-- ===========================================================
CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    custom_field_id TEXT NOT NULL,
    value TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (custom_field_id) REFERENCES custom_fields(custom_field_id)
);
