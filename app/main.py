from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback

# Imports handling package and root execution
try:
    from app.db import init_db, run_query
    from app.llm_engine import generate_sql
    from app.anomaly import get_anomalies
except ImportError:
    from db import init_db, run_query
    from llm_engine import generate_sql
    from anomaly import get_anomalies


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        print("[DB] Initialized database successfully.")
    except Exception as e:
        print(f"[DB Error] Initialization failed: {e}")
    yield


app = FastAPI(
    title="AI Support Ticket Intelligence API",
    version="1.0.0",
    lifespan=lifespan
)


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "model_provider": "Groq Free Tier (Llama-3.3-70b)"
    }


@app.post("/query")
def natural_language_query(req: QueryRequest):
    if not req.question:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        generated_sql = generate_sql(req.question)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM Translation failed: {str(e)}")

    data, err = run_query(generated_sql)
    if err:
        raise HTTPException(status_code=400, detail=f"SQL Execution Error: {err} | Query was: {generated_sql}")

    return {
        "question": req.question,
        "generated_sql": generated_sql,
        "result_count": len(data),
        "data": data
    }


@app.get("/anomalies")
def detect_anomalies():
    try:
        return get_anomalies()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Anomaly scanning failed: {str(e)}")