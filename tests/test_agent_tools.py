from fastapi.testclient import TestClient

from src.backend.app import app


def test_agent_tools_endpoint_describes_openapi_operations() -> None:
    client = TestClient(app)

    response = client.get("/agent/tools")

    assert response.status_code == 200

    tools_by_url = {tool["url"]: tool for tool in response.json()["tools"]}
    assert tools_by_url["/health"] == {
        "name": "health_health_get",
        "description": "Health",
        "method": "GET",
        "url": "/health",
        "input_schema": {},
        "output_schema": {},
    }
    assert tools_by_url["/agent/tools"]["method"] == "GET"
    assert "/{path}" not in tools_by_url
