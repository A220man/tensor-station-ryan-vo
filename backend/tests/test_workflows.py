import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_workflow(client):
    payload = {
        "name": "Test Workflow",
        "description": "A test workflow",
        "nodes": [
            {
                "id": "node-1",
                "type": "checkpoint_loader",
                "position": {"x": 100, "y": 100},
                "data": {"model_name": "sdxl"}
            }
        ],
        "edges": []
    }
    response = await client.post("/api/v1/workflows", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Workflow"
    assert data["description"] == "A test workflow"
    assert len(data["nodes"]) == 1
    assert "id" in data
    return data["id"]


@pytest.mark.asyncio
async def test_list_workflows(client):
    response = await client.get("/api/v1/workflows")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_workflow(client):
    # First create
    payload = {"name": "Get Test", "nodes": [], "edges": []}
    create_resp = await client.post("/api/v1/workflows", json=payload)
    wf_id = create_resp.json()["id"]

    # Then get
    response = await client.get(f"/api/v1/workflows/{wf_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == wf_id
    assert data["name"] == "Get Test"


@pytest.mark.asyncio
async def test_update_workflow(client):
    payload = {"name": "Update Test", "nodes": [], "edges": []}
    create_resp = await client.post("/api/v1/workflows", json=payload)
    wf_id = create_resp.json()["id"]

    update_payload = {"name": "Updated Name"}
    response = await client.patch(f"/api/v1/workflows/{wf_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_workflow(client):
    payload = {"name": "Delete Test", "nodes": [], "edges": []}
    create_resp = await client.post("/api/v1/workflows", json=payload)
    wf_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/workflows/{wf_id}")
    assert response.status_code == 204

    # Verify deleted
    get_resp = await client.get(f"/api/v1/workflows/{wf_id}")
    assert get_resp.status_code == 404