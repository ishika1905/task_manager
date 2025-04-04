from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/tasks/")
    assert response.status_code in [401, 403]  # Unauthorized access without token
