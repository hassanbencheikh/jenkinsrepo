import pytest
from app import app as flask_app

@pytest.fixture
def client():
    # Create a test client using the Flask application context
    with flask_app.test_client() as client:
        yield client

# --- Tests for /add ---
def test_add(client):
    """Test the add endpoint."""
    rv = client.get('/add?a=10&b=5')
    assert rv.status_code == 200
    assert rv.json == {"result": 15.0}

def test_add_missing_params(client):
    """Test the add endpoint with missing parameters."""
    rv = client.get('/add?a=10')
    assert rv.status_code == 400
    assert "error" in rv.json

# --- Tests for /subtract ---
def test_subtract(client):
    """Test the subtract endpoint."""
    rv = client.get('/subtract?a=10&b=5')
    assert rv.status_code == 200
    assert rv.json == {"result": 5.0}

# --- Tests for /multiply ---
def test_multiply(client):
    """Test the multiply endpoint."""
    rv = client.get('/multiply?a=10&b=5')
    assert rv.status_code == 200
    assert rv.json == {"result": 50.0}

# --- Tests for /divide ---
def test_divide(client):
    """Test the divide endpoint."""
    rv = client.get('/divide?a=10&b=5')
    assert rv.status_code == 200
    assert rv.json == {"result": 2.0}

def test_divide_by_zero(client):
    """Test dividing by zero."""
    rv = client.get('/divide?a=10&b=0')
    assert rv.status_code == 400
    assert rv.json == {"error": "Division by zero is not allowed."}

def test_divide_missing_params(client):
    """Test the divide endpoint with missing parameters."""
    rv = client.get('/divide?b=5')
    assert rv.status_code == 400
    assert "error" in rv.json
