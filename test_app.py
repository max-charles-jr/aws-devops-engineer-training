import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'AWS DevOps Demo Application' in response.data

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['service'] == 'aws-devops-demo'

def test_info_endpoint(client):
    """Test the info API endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['application'] == 'AWS DevOps Demo'
    assert 'version' in json_data
