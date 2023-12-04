from src import controller
import pytest
from flask import render_template
import pytest

@pytest.fixture
def client():
    with controller.app.test_client() as client:
        yield client

@pytest.mark.integration
def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/index.html')

@pytest.mark.integration
def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/login.html')
    
@pytest.mark.integration
def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/register.html')
    
@pytest.mark.integration
def test_404_error(client):
    response = client.get('/nonexistentroute')
    assert response.status_code == 404

@pytest.mark.integration
def test_500_error(client):
    response = client.get('/book/invaliduuid')
    assert response.status_code == 500