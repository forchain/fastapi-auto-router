from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_auto_router import AutoRouter
import pytest
import os

@pytest.fixture
def app():
    app = FastAPI()
    return app

@pytest.fixture
def example_router_dir():
    # Get the path to the examples/routers directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "examples", "routers")

@pytest.fixture
def test_client(app, example_router_dir):
    # Initialize and load routers
    auto_router = AutoRouter(
        app=app,
        routers_dir=example_router_dir,
        api_prefix="/api/v1"
    )
    auto_router.load_routers()
    return TestClient(app)

def test_auto_router_initialization(app):
    router = AutoRouter(
        app=app,
        routers_dir="test_routers",
        api_prefix="/api/v1"
    )
    assert router.api_prefix == "/api/v1"
    assert router.routers_dir == "test_routers"

def test_list_users_endpoint(test_client):
    """Test the /api/v1/user-management/users endpoint"""
    response = test_client.get("/api/v1/user-management/users")
    assert response.status_code == 200
    assert response.json() == {"message": "List users"}

def test_user_profile_endpoint(test_client):
    """Test the /api/v1/user-management/{user_id}/profile endpoint"""
    user_id = "123"
    response = test_client.get(f"/api/v1/user-management/{user_id}/profile")
    assert response.status_code == 200
    assert response.json() == {"message": f"Get profile for user {user_id}"} 