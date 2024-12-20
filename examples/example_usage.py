from fastapi import FastAPI
from fastapi_auto_router import AutoRouter

def create_app():
    app = FastAPI()
    
    # Initialize and load routers
    auto_router = AutoRouter(
        app=app,
        routers_dir="routers",  # relative to current file
        api_prefix="/api/v1"
    )
    auto_router.load_routers()
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 