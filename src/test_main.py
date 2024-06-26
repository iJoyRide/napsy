from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# Tests for post_website
def test_functional():
    response = client.post("/post", json={"websites": ["google.com", "facebook.com", "example.com"]})
    assert response.status_code == 200
    assert response.json() == {
        "ip_addresses": ["google.com", "facebook.com", "example.com"]
    }

# Tests for predict
def test_predict():
    response = client.post("/predict", json = {
        "http://google.com": False,
        "http://example.com": True
    })
    assert response.status_code == 200
    assert response.json() == {
        "http://google.com": "safe",
        "http://example.com": "unsafe"
    }

def test_non_dict_input():
    response = client.post("/predict", json=[])
    assert response.status_code == 400
    assert response.json() == {"detail": "Data must be a dictionary"}

def test_non_boolean_values():
    response = client.post("/predict", json={"http://google.com": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid value for http://google.com. Expected a boolean."}
    