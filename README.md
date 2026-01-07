# 🧩 Asana Workspace Simulation — B2B SaaS Dataset Generator  

### 🧠 Research Scientist Internship Take-Home Project  
**Author:** GIshwar Gajakosh  
**Duration:** January 2026  
**Repository:** https://github.com/GIshwar/asana-simulation.git
**Database Output:** `output/asana_simulation.sqlite`

---

## 🚀 Overview  

This project simulates a **realistic Asana workspace dataset** representing a B2B SaaS company with 5,000–10,000 employees.  
The dataset emulates the structure, relationships, and behaviors observed in actual Asana environments — including teams, users, projects, tasks, subtasks, comments, tags, attachments, and more.

It aims to support **productivity research, LLM modeling, and reinforcement learning experiments** in structured workflow environments.

> 🎯 **Goal:** Create a scalable, realistic, and fully relational Asana-like simulation suitable for data science and research use.

---

### 🧩 ER Diagram  

[![ER Diagram](docs/asana_er_diagram.png)](docs/asana_er_diagram.png)



## 🏗️ Architecture Overview  

### 📁 Folder Structure  

asana-simulation/
├── README.md
├── requirements.txt
├── schema.sql
├── .env.example
├── src/
│   ├── main.py
│   ├── scrapers/
│   │   ├── company_scraper.py
│   │   └── names_scraper.py
│   ├── generators/
│   │   ├── organization.py   
│   │   ├── users.py
│   │   ├── teams.py
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   ├── subtasks.py
│   │   ├── comments.py
│   │   ├── tags.py
│   │   ├── sections.py
│   │   ├── attachments.py
│   │   └── custom_fields.py
│   ├── utils/
│   │   ├── llm_helper.py
│   │   ├── date_utils.py
│   │   └── random_utils.py
├── prompts/
│   └── task_prompts.txt
├── docs/
│   ├── documentation.md
│   └── er_diagram.png
└── output/
    └── asana_simulation.sqlite


---

## 🧠 Key Features  

| Feature | Description |
|----------|--------------|
| 🧱 **11 Interconnected Entities** | Realistic Asana hierarchy — org → teams → users → projects → tasks → subtasks → comments → tags → attachments → custom fields → sections |
| 🤖 **LLM-Generated Text** | Optional GPT-based generation for task descriptions and comments |
| 📈 **Statistical Realism** | Team sizes, project durations, and due dates follow industry research patterns |
| 🕒 **Temporal Consistency** | Tasks can’t finish before creation; dependencies are validated |
| 🔄 **Reproducible Simulation** | Configurable via `.env` and modular Python structure |
| 💬 **Research Ready** | Supports analysis of team productivity, communication patterns, and RL agent simulations |

---

## ⚙️ Setup Instructions  

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/GIshwar/asana-simulation.git
cd asana-simulation

2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate  # On Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Copy .env.example → .env
and replace your API key:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


⚠️ Never commit .env to GitHub — it’s listed in .gitignore.

5️⃣ Run Simulation
python src/main.py


Expected output:

🎉 Simulation complete!
📦 Database ready at: output/asana_simulation.sqlite
⏱️  Time taken: ~26 minutes

🧩 Database Schema Overview

The schema captures full relational integrity among entities:

Table	Description
organizations	Company-level metadata
teams	Departments / functional units
users	Employees with role + team mapping
projects	Projects owned by teams
sections	Logical grouping of project tasks
tasks	Main actionable work items
subtasks	Nested tasks under parent
comments	Collaboration and feedback threads
tags	Categorization labels
attachments	Files linked to tasks
custom_fields	Extra metadata for projects
task_tags	Many-to-many linking between tasks and tags

📊 Simulation Statistics
Entity	Records
Organizations	1
Teams	40
Users	8,000
Projects	261
Sections	1,145
Tasks	20,000
Subtasks	26,487
Comments	48,606
Tags	40
Task-Tag Links	30,100
Attachments	19,928
Custom Fields	933

🕒 Runtime: ~26 min on local CPU (Python 3.9, 16GB RAM)

🔬 Evaluation Mapping
Criterion	Weight	Implementation
Data Realism	45%	Industry-based entity distributions, LLM content generation, Asana-like hierarchies
Methodology Rigor	35%	Documented logic, foreign key constraints, time validation, faker + OpenAI blending
Documentation Quality	10%	README, technical docs, ER diagram
Code Quality	10%	Modular structure, reusable utilities, externalized configs

💡 Example Use Cases

✅ Benchmarking for LLM workflow planners
✅ Training RL agents for task prioritization
✅ Building visualization dashboards
✅ Studying human–AI productivity patterns

🧱 Tech Stack
Category	Tool
Language	Python 3.9+
Database	SQLite
Libraries	Faker, tqdm, OpenAI, pandas, python-dotenv
Visualization	ER diagram
Environment	Local / Google Colab / Kaggle (supported)

📁 Reproducibility

To regenerate the entire dataset:

pip install -r requirements.txt
python src/main.py


The database will be created at:

output/asana_simulation.sqlite

🧩 Credits & Acknowledgements

Developed as part of the Research Scientist Internship — Take-Home Assignment.
Inspired by Asana’s Anatomy of Work reports, YC company data, and synthetic dataset generation best practices.

📜 License

This project is licensed under the MIT License — you’re free to use, modify, and distribute with attribution.

🧠 Author

GIshwar Gajakosh
https://github.com/GIshwar
Aspiring Research Scientist | AI & Data Simulation Enthusiast

⭐ If you found this project insightful, consider starring the repo!