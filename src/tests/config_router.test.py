from fastapi.testclient import TestClient
from main import app  # Replace "app" with the name of your FastAPI instance

client = TestClient(app)

def test_create_config():
    new_config = {
        "user_id": "user123",
        "config_data": {"key": "value"}
    }
    response = client.post("/config/", json=new_config)
    assert response.status_code == 200
    assert response.json()["user_id"] == "user123"

def test_read_config():
    response = client.get("/config/user123")
    assert response.status_code == 200
    assert response.json()["user_id"] == "user123"

def test_update_config():
    updated_config = {
        "user_id": "user123",
        "config_data": {"updated_key": "updated_value"}
    }
    response = client.put("/config/user123", json=updated_config)
    assert response.status_code == 200
    assert response.json()["config_data"]["updated_key"] == "updated_value"

def test_delete_config():
    response = client.delete("/config/user123")
    assert response.status_code == 200
    assert response.json()["message"] == "Config deleted successfully"
