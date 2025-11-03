from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_auto_router import AutoRouter
import pytest
import os
from pathlib import Path

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

def test_base_path_with_relative_routers_dir(app):
    """Test that base_path is used when routers_dir is relative"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Use base_path with relative routers_dir
    auto_router = AutoRouter(
        app=app,
        routers_dir="examples/routers",
        api_prefix="/api/v1",
        base_path=project_root
    )
    auto_router.load_routers()
    
    client = TestClient(app)
    response = client.get("/api/v1/user-management/users")
    assert response.status_code == 200
    assert response.json() == {"message": "List users"}

def test_base_path_with_absolute_routers_dir(app):
    """Test that base_path is ignored when routers_dir is absolute"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    absolute_routers_dir = os.path.join(project_root, "examples", "routers")
    
    # Use absolute routers_dir - base_path should be ignored
    auto_router = AutoRouter(
        app=app,
        routers_dir=absolute_routers_dir,
        api_prefix="/api/v1",
        base_path="/this/path/should/be/ignored"
    )
    auto_router.load_routers()
    
    client = TestClient(app)
    response = client.get("/api/v1/user-management/users")
    assert response.status_code == 200
    assert response.json() == {"message": "List users"}

def test_base_path_default_behavior(app):
    """Test that base_path defaults to current working directory"""
    auto_router = AutoRouter(
        app=app,
        routers_dir="test_routers",
        api_prefix="/api"
    )
    
    # Verify base_path defaults to current working directory
    assert auto_router.base_path == os.getcwd()

def test_base_path_custom_value(app):
    """Test that custom base_path is stored correctly"""
    custom_path = "/custom/base/path"
    auto_router = AutoRouter(
        app=app,
        routers_dir="routers",
        api_prefix="/api",
        base_path=custom_path
    )
    
    # Verify custom base_path is stored
    assert auto_router.base_path == custom_path

def test_base_path_with_path_object(app):
    """Test that base_path works with Path objects converted to string"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = Path(current_dir).parent
    
    auto_router = AutoRouter(
        app=app,
        routers_dir="examples/routers",
        api_prefix="/api/v1",
        base_path=str(project_root)
    )
    auto_router.load_routers()
    
    client = TestClient(app)
    response = client.get("/api/v1/user-management/users")
    assert response.status_code == 200
    assert response.json() == {"message": "List users"} 