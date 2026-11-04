from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Depends, Request
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, UTC
import uuid
import asyncio
import random

router = APIRouter(tags=["inference"])

class InferenceRequest(BaseModel):
    workflow_id: str
    model_id: Optional[str] = None
    prompt: str = Field(..., min_length=1)
    negative_prompt: str = ""
    width: int = Field(512, ge=64, le=2048, multiple_of=64)
    height: int = Field(512, ge=64, le=2048, multiple_of=64)
    steps: int = Field(20, ge=1, le=100)
    cfg_scale: float = Field(7.0, ge=0.0, le=30.0)
    sampler: str = "euler"
    scheduler: str = "normal"
    seed: Optional[int] = None
    batch_size: int = Field(1, ge=1, le=4)
    
    model_config = ConfigDict(protected_namespaces=())

class InferenceResponse(BaseModel):
    execution_id: str
    status: str
    created_at: datetime

class ExecutionStatus(BaseModel):
    execution_id: str
    status: str
    progress: float = 0.0
    current_step: int = 0
    total_steps: int = 0
    result_urls: List[str] = []
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

_executions: Dict[str, Dict] = {}

async def validate_model(request: Request) -> Optional[str]:
    """Validate that the model exists in the registry."""
    # Extract model_id from request body
    body = await request.json()
    model_id = body.get("model_id")
    if model_id is None:
        return None
    # Import here to avoid circular imports
    from app.api.models import _models
    if model_id not in _models:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {model_id} not found in registry"
        )
    return model_id

@router.post("/inference", response_model=InferenceResponse, status_code=status.HTTP_202_ACCEPTED)
async def queue_inference(request: InferenceRequest, background_tasks: BackgroundTasks, validated_model_id: Optional[str] = Depends(validate_model)):
    execution_id = str(uuid.uuid4())
    now = datetime.now(UTC)
    _executions[execution_id] = {
        "execution_id": execution_id, "workflow_id": request.workflow_id, "model_id": request.model_id,
        "prompt": request.prompt, "negative_prompt": request.negative_prompt, "width": request.width,
        "height": request.height, "steps": request.steps, "cfg_scale": request.cfg_scale,
        "sampler": request.sampler, "scheduler": request.scheduler, "seed": request.seed,
        "batch_size": request.batch_size, "status": "queued", "progress": 0.0, "current_step": 0,
        "total_steps": request.steps, "result_urls": [], "error": None, "created_at": now,
        "started_at": None, "completed_at": None,
    }
    background_tasks.add_task(run_inference, execution_id)
    return InferenceResponse(execution_id=execution_id, status="queued", created_at=now)

async def run_inference(execution_id: str):
    exec_data = _executions.get(execution_id)
    if not exec_data: return
    exec_data["status"] = "running"
    exec_data["started_at"] = datetime.now(UTC)
    try:
        total_steps = exec_data["total_steps"]
        for step in range(total_steps):
            await asyncio.sleep(0.05)
            exec_data["current_step"] = step + 1
            exec_data["progress"] = (step + 1) / total_steps
            if random.random() < 0.01:
                raise RuntimeError("Simulated inference failure")
        exec_data["status"] = "completed"
        exec_data["completed_at"] = datetime.now(UTC)
        batch_size = exec_data["batch_size"]
        exec_data["result_urls"] = [f"/outputs/{execution_id}_{i}.png" for i in range(batch_size)]
    except Exception as e:
        exec_data["status"] = "failed"
        exec_data["error"] = str(e)
        exec_data["completed_at"] = datetime.now(UTC)

@router.get("/inference/{execution_id}", response_model=ExecutionStatus)
async def get_execution_status(execution_id: str):
    if execution_id not in _executions:
        raise HTTPException(status_code=404, detail="Execution not found")
    return ExecutionStatus(**_executions[execution_id])

@router.get("/inference", response_model=List[ExecutionStatus])
async def list_executions(limit: int = 50, offset: int = 0):
    items = list(_executions.values())[offset : offset + limit]
    return [ExecutionStatus(**e) for e in items]

@router.post("/inference/{execution_id}/cancel")
async def cancel_inference(execution_id: str):
    if execution_id not in _executions:
        raise HTTPException(status_code=404, detail="Execution not found")
    if _executions[execution_id]["status"] in ("queued", "running"):
        _executions[execution_id]["status"] = "cancelled"
        _executions[execution_id]["completed_at"] = datetime.now(UTC)
    return {"status": "cancelled", "execution_id": execution_id}
