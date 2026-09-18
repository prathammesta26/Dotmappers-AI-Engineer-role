# AI Support Ticket Intelligence Platform

An end-to-end operational intelligence platform designed to ingest enterprise support ticket datasets, translate conversational English into executable SQLite queries using LLMs, and dynamically flag statistical and operational bottlenecks.

Built for the **DOTMappers AI Engineer Technical Assessment**.

---

## 1. System Architecture

The platform follows a decoupled, production-style architecture:

* **Storage Layer (`app/db.py`):** Ingests `support_tickets.csv` into an embedded, relational SQLite database (`tickets` table) on startup.
* **LLM Engine (`app/llm_engine.py`):** Converts natural language queries into schema-constrained SQL using Groq's high-speed inference (`llama3-8b-8192`) with a zero-cost deterministic fallback.
* **Anomaly Detection Engine (`app/anomaly.py`):** Combines statistical outlier detection ($\mu + 2.5\sigma$ on resolution hours) with heuristic operational rules (unresolved high/critical tickets).
* **Backend API (`app/main.py`):** FastAPI application exposing documented REST endpoints (`/health`, `/query`, `/anomalies`).
* **Frontend UI (`ui.py`):** Streamlit dashboard providing interactive querying, instant data tables, and operational anomaly reporting.
* **Single-Command Orchestrator (`run.py`):** Simultaneously starts both the backend API and frontend UI with a single command.

---

## 2. Directory Structure

```text
dotmappers-ticket-system/
├── app/
│   ├── __init__.py          # Module anchor
│   ├── main.py              # FastAPI application & lifespan management
│   ├── db.py                # SQLite ingestion & query execution
│   ├── llm_engine.py        # Text-to-SQL logic & Groq integration
│   └── anomaly.py           # Statistical and operational anomaly algorithms
├── support_tickets.csv      # Raw operational dataset (500 tickets)
├── ui.py                    # Streamlit analytical dashboard
├── run.py                   # Single-command launcher script
├── requirements.txt         # Project dependencies
├── .env                     # Local environment variables (API keys)
├── .gitignore               # Git security filters
└── README.md                # Project documentation

<img width="1426" height="752" alt="Dashboard 1" src="https://github.com/user-attachments/assets/488003ae-c2e4-46b9-bd2c-b2944b89a7bf" />
<img width="1198" height="740" alt="Dashboard 2" src="https://github.com/user-attachments/assets/7f04e130-5aaf-401f-8817-4fd05499ebf2" />

