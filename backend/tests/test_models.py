import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_register_model(client):
    payload = {
        "name": "Test Model",
        "type": "checkpoint",
        "path": "/models/sdxl.safetensors",
        "size_bytes": 6500000000,
        "format": "safetensors",
        "metadata": {"architecture": "SDXL"}
    }
    response = await client.post("/api/v1/models", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Model"
    assert data["type"] == "checkpoint"
    assert "id" in data
    return data["id"]


@pytest.mark.asyncio
async def test_list_models(client):
    response = await client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_model(client):
    payload = {
        "name": "Get Model",
        "type": "lora",
        "path": "/models/lora.safetensors",
        "size_bytes": 100000000,
        "format": "safetensors"
    }
    create_resp = await client.post("/api/v1/models", json=payload)
    model_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/models/{model_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == model_id


@pytest.mark.asyncio
async def test_load_unload_model(client):
    payload = {
        "name": "Load Model",
        "type": "checkpoint",
        "path": "/models/test.safetensors",
        "size_bytes": 1000000000,
        "format": "safetensors"
    }
    create_resp = await client.post("/api/v1/models", json=payload)
    model_id = create_resp.json()["id"]

    # Load
    load_resp = await client.post("/api/v1/models/load", json={"model_id": model_id, "device": "cuda"})
    assert load_resp.status_code == 200
    data = load_resp.json()
    assert data["model_id"] == model_id
    assert data["status"] == "loaded"

    # List loaded
    list_resp = await client.get("/api/v1/models/loaded/list")
    assert list_resp.status_code == 200
    loaded = list_resp.json()
    assert any(m["model_id"] == model_id for m in loaded)

    # Unload
    unload_resp = await client.post(f"/api/v1/models/{model_id}/unload")
    assert unload_resp.status_code == 200