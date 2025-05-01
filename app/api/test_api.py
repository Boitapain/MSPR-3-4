import pytest
from app.api.api import app  # Adjust the import according to your project structure

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_endpoint(client):
    response = client.get('/api/endpoint')
    assert response.status_code == 200, "Status code should be 200"
    assert response.json == {"key": "value"}, "Response JSON does not match expected output"

def test_api_endpoint_not_found(client):
    response = client.get('/api/nonexistent')
    assert response.status_code == 404, "Status code should be 404 for nonexistent endpoint"
