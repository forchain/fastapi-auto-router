from fastapi import FastAPI
from fastapi_auto_router import AutoRouter

app = FastAPI()

# Initialize and load routers
auto_router = AutoRouter(
    app=app,
    routers_dir="routers",
    api_prefix="/api/v1"
)
auto_router.load_routers() 