# app/routers/workflow.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.mock_llm import get_mock_llm_response

router = APIRouter()

class WorkflowRequest(BaseModel):
    query: str
    context: str = ""  # optional context from KnowledgeBase

@router.post("/run-workflow")
def run_workflow(req: WorkflowRequest):
    # Use mock LLM to generate a response
    response = get_mock_llm_response(req.query, req.context)
    return {"response": response}
