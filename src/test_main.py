from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_functional():
    response = client.post("/post", json={"websites": ["google.com", "facebook.com", "example.com"]})
    assert response.status_code == 200
    assert response.json() == {
        "ip_addresses": ["google.com", "facebook.com", "example.com"]
    }

def test_not_url():
    response = client.post("/post", json={"websites": ["google.com", "nonexistentdomain", "example.com"]})
    assert response.status_code == 200
    assert response.json() == {
        "ip_addresses": ["google.com", "0", "example.com"]
    }






