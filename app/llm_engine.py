import os
import re
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Read .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SYSTEM_PROMPT = """You are an expert Data Engineer. Convert user natural language questions into safe SQLite queries.
The table name is 'tickets'.
Schema:
- ticket_id (TEXT)
- created_at (TEXT, format 'YYYY-MM-DD HH:MM')
- category (TEXT: 'Billing', 'Technical', 'General')
- priority (TEXT: 'Low', 'Medium', 'High', 'Critical')
- status (TEXT: 'Open', 'Resolved', 'Escalated')
- response_time_hrs (REAL)
- resolution_time_hrs (REAL, NULL if unresolved)
- agent_id (TEXT, e.g., 'AGT-01')
- customer_rating (INTEGER: 1 to 5, NULL if unresolved)
- issue_summary (TEXT)

Rules:
1. Return ONLY the raw SQL query enclosed in ```sql ... ```. No conversational text.
2. Only write SELECT statements. Reject any UPDATE, DELETE, or DROP.
3. Handle case-insensitive searches where appropriate using LOWER().
"""

def generate_sql(user_question: str) -> str:
    # Rule-based fallback for standard queries if API fails
    q = user_question.lower()
    fallback_sql = "SELECT * FROM tickets LIMIT 5;"
    if "open" in q:
        fallback_sql = "SELECT COUNT(*) AS open_tickets_count FROM tickets WHERE status = 'Open';"
    elif "lowest average" in q or "lowest rating" in q:
        fallback_sql = "SELECT agent_id, AVG(customer_rating) as avg_rating FROM tickets WHERE customer_rating IS NOT NULL GROUP BY agent_id ORDER BY avg_rating ASC LIMIT 1;"
    elif "resolution time" in q and "category" in q:
        fallback_sql = "SELECT category, AVG(resolution_time_hrs) as avg_resolution_time FROM tickets WHERE status = 'Resolved' GROUP BY category;"

    if not GROQ_API_KEY:
        return fallback_sql

    client = Groq(api_key=GROQ_API_KEY)
    
    # Try the most common active Groq model names in order
    candidate_models = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
    
    for model_name in candidate_models:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.0
            )
            raw_text = response.choices[0].message.content
            match = re.search(r"```sql(.*?)```", raw_text, re.DOTALL)
            if match:
                return match.group(1).strip()
            return raw_text.strip().replace(";", "")
        except Exception:
            continue

    # If all remote models fail to respond, use the deterministic fallback query
    return fallback_sql