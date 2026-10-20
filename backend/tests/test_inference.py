import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_queue_inference(client):
    # First create a workflow
    wf_payload = {"name": "Inference WF", "nodes": [], "edges": []}
    wf_resp = await client.post("/api/v1/workflows", json=wf_payload)
    wf_id = wf_resp.json()["id"]

    # Queue inference
    payload = {
        "workflow_id": wf_id,
        "prompt": "a beautiful landscape",
        "width": 512,
        "height": 512,
        "steps": 10,
        "cfg_scale": 7.0,
        "sampler": "euler",
        "scheduler": "normal"
    }
    response = await client.post("/api/v1/inference", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "queued"
    assert "execution_id" in data
    return data["execution_id"]


@pytest.mark.asyncio
async def test_get_execution_status(client):
    # Create workflow and queue inference
    wf_payload = {"name": "Status WF", "nodes": [], "edges": []}
    wf_resp = await client.post("/api/v1/workflows", json=wf_payload)
    wf_id = wf_resp.json()["id"]

    inf_payload = {"workflow_id": wf_id, "prompt": "test", "steps": 5}
    inf_resp = await client.post("/api/v1/inference", json=inf_payload)
    exec_id = inf_resp.json()["execution_id"]

    # Poll status
    response = await client.get(f"/api/v1/inference/{exec_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["execution_id"] == exec_id
    assert data["status"] in ("queued", "running", "completed")


@pytest.mark.asyncio
async def test_list_executions(client):
    response = await client.get("/api/v1/inference")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_cancel_inference(client):
    wf_payload = {"name": "Cancel WF", "nodes": [], "edges": []}
    wf_resp = await client.post("/api/v1/workflows", json=wf_payload)
    wf_id = wf_resp.json()["id"]

    inf_payload = {"workflow_id": wf_id, "prompt": "cancel test", "steps": 20}
    inf_resp = await client.post("/api/v1/inference", json=inf_payload)
    exec_id = inf_resp.json()["execution_id"]

    response = await client.post(f"/api/v1/inference/{exec_id}/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cancelled"