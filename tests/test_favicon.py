from fastapi.testclient import TestClient

from src.backend.app import FRONTEND_SOURCE, app


def test_favicon_routes_serve_the_replaceable_png_asset() -> None:
    client = TestClient(app)
    expected = (FRONTEND_SOURCE / "favicon.png").read_bytes()

    for route in ("/favicon.ico", "/favicon.png"):
        response = client.get(route)

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert response.content == expected
        assert response.content.startswith(b"\x89PNG\r\n\x1a\n")
