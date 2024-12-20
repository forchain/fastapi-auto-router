# FastAPI Auto Router

Automatic router configuration for FastAPI based on filesystem structure.

## Installation

```bash
pip install fastapi-auto-router
```

## Usage

1. Create your router files in a directory structure that matches your desired API paths:

```
your_project/
└── routers/
    └── user_management
        ├── users.py
        └── {user_id}/
                └── profile.py
```

2. In your router files, create FastAPI routers:

routers/user_management/users.py

```python
from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_users():
    return {"message": "List users"}
```

3. In your main FastAPI application, use AutoRouter:

```python
from fastapi import FastAPI
from fastapi_auto_router import AutoRouter

app = FastAPI()
# Initialize and load routers
auto_router = AutoRouter(
    app=app,
    routers_dir="routers",  # Path to your routers directory
    api_prefix="/api/v1"  # Optional: prefix for all routes
)
auto_router.load_routers()
```

This will create the following routes:

- `/api/v1/user-management/users`
- `/api/v1/user-management/{user_id}/profile`

## Features

- Automatic route configuration based on filesystem structure
- Converts underscores to hyphens in route paths
- Supports path parameters using {parameter_name} folders
- Customizable API prefix
- Works with any FastAPI application

## License

MIT License
