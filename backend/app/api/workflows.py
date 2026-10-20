from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

router = APIRouter(tags=["workflows"])


class NodeData(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]


class EdgeData(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None


class WorkflowCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    nodes: List[NodeData] = []
    edges: List[EdgeData] = []


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    nodes: Optional[List[NodeData]] = None
    edges: Optional[List[EdgeData]] = None


class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    nodes: List[NodeData]
    edges: List[EdgeData]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# In-memory storage (replace with DB in next phase)
_workflows: Dict[str, Dict] = {}


@router.post("/workflows", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(workflow: WorkflowCreate):
    workflow_id = str(uuid.uuid4())
    now = datetime.utcnow()
    data = workflow.model_dump()
    data.update({"id": workflow_id, "created_at": now, "updated_at": now})
    _workflows[workflow_id] = data
    return WorkflowResponse(**data)


@router.get("/workflows", response_model=List[WorkflowResponse])
async def list_workflows(limit: int = 50, offset: int = 0):
    items = list(_workflows.values())[offset : offset + limit]
    return [WorkflowResponse(**w) for w in items]


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    if workflow_id not in _workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return WorkflowResponse(**_workflows[workflow_id])


@router.patch("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(workflow_id: str, workflow: WorkflowUpdate):
    if workflow_id not in _workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    data = _workflows[workflow_id]
    update_data = workflow.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    data.update(update_data)
    return WorkflowResponse(**data)


@router.delete("/workflows/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(workflow_id: str):
    if workflow_id not in _workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    del _workflows[workflow_id]