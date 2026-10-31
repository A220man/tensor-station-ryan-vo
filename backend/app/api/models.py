from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, UTC
import uuid

router = APIRouter(tags=["models"])


class ModelInfo(BaseModel):
    id: str
    name: str
    type: str  # checkpoint, lora, vae, clip, controlnet, upscaler
    path: str
    size_bytes: int
    format: str  # safetensors, pth, ckpt, etc.
    metadata: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ModelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: str
    path: str
    size_bytes: int
    format: str
    metadata: Dict[str, Any] = {}


class ModelLoadRequest(BaseModel):
    model_id: str
    device: str = "cuda"
    dtype: str = "float16"

    model_config = {"protected_namespaces": ()}


class ModelLoadResponse(BaseModel):
    model_id: str
    status: str  # loaded, loading, error
    device: str
    vram_used_mb: float
    load_time_ms: float

    model_config = {"protected_namespaces": ()}


# In-memory storage
_models: Dict[str, Dict] = {}
_loaded_models: Dict[str, Dict] = {}


@router.post("/models", response_model=ModelInfo, status_code=status.HTTP_201_CREATED)
async def register_model(model: ModelCreate):
    model_id = str(uuid.uuid4())
    now = datetime.now(UTC)
    data = model.model_dump()
    data.update({"id": model_id, "created_at": now, "updated_at": now})
    _models[model_id] = data
    return ModelInfo(**data)


@router.get("/models", response_model=List[ModelInfo])
async def list_models(limit: int = 50, offset: int = 0, type: Optional[str] = None):
    items = list(_models.values())
    if type:
        items = [m for m in items if m["type"] == type]
    items = items[offset : offset + limit]
    return [ModelInfo(**m) for m in items]


@router.get("/models/{model_id}", response_model=ModelInfo)
async def get_model(model_id: str):
    if model_id not in _models:
        raise HTTPException(status_code=404, detail="Model not found")
    return ModelInfo(**_models[model_id])


@router.post("/models/load", response_model=ModelLoadResponse)
async def load_model(request: ModelLoadRequest):
    if request.model_id not in _models:
        raise HTTPException(status_code=404, detail="Model not found")

    # Simulate model loading
    import time
    start = time.perf_counter()
    # In real implementation, load model with torch/safetensors
    load_time = (time.perf_counter() - start) * 1000

    _loaded_models[request.model_id] = {
        "device": request.device,
        "dtype": request.dtype,
        "loaded_at": datetime.now(UTC),
    }

    return ModelLoadResponse(
        model_id=request.model_id,
        status="loaded",
        device=request.device,
        vram_used_mb=0.0,  # Would query actual VRAM
        load_time_ms=load_time,
    )


@router.post("/models/{model_id}/unload")
async def unload_model(model_id: str):
    if model_id in _loaded_models:
        del _loaded_models[model_id]
    return {"status": "unloaded", "model_id": model_id}


@router.get("/models/loaded/list")
async def list_loaded_models():
    return [
        {"model_id": mid, **info}
        for mid, info in _loaded_models.items()
    ]