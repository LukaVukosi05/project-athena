from fastapi.testclient import TestClient

from app.main import app


def test_past_paper_content_api_is_inactive_during_curriculum_reset():
    with TestClient(app) as client:
        assert client.get("/api/v1/past-papers").status_code == 404


def test_development_frontend_assets_are_not_cached_and_show_only_sequences():
    with TestClient(app) as client:
        dashboard = client.get("/dashboard.html")
        script = client.get("/js/pages/dashboard.js")
    assert "no-store" in dashboard.headers["cache-control"]
    assert "no-store" in script.headers["cache-control"]
    assert "Sequences and Series" in script.text
    assert "Paper 2 lessons" not in script.text
