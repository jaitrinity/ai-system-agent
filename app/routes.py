from fastapi import APIRouter
from app.agent import run_agent

router = APIRouter()

@router.post("/ask")
def ask_agent(item: dict):
    query = item.get("message")
    result = run_agent(query)
    return {"response": result}
