from fastapi.testclient import TestClient
from backend.main import app
import io

client = TestClient(app)

def test_analyze_endpoint():
    resume = io.BytesIO(b"Experienced Python developer with FastAPI expertise.")
    jd = io.BytesIO(b"Looking for a backend engineer with Python and FastAPI.")
    response = client.post("/analyze/", files={
        "resume": ("resume.txt", resume, "text/plain"),
        "job_description": ("jd.txt", jd, "text/plain")
    })
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert "match_percent" in data
