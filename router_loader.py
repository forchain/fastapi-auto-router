import importlib
import os
from pathlib import Path
from typing import List, Tuple

from fastapi import APIRouter

def convert_path_to_route(path: str) -> str:
    """Convert filesystem path to API route path"""
    # Remove .py extension
    if path.endswith('.py'):
        path = path[:-3]
    # Convert underscores to hyphens for non-parameter parts
    parts = path.split('/')
    converted_parts = []
    for part in parts:
        if part.startswith('{') and part.endswith('}'):
            converted_parts.append(part)
        else:
            converted_parts.append(part.replace('_', '-'))
    return '/'.join(converted_parts)

def get_module_path(file_path: str, base_path: str) -> str:
    """Convert file path to module import path"""
    relative_path = os.path.relpath(file_path, base_path)
    return relative_path.replace('/', '.').replace('\\', '.').replace('.py', '')

def load_routers(routers_dir: str = "routers") -> APIRouter:
    main_router = APIRouter()
    base_path = os.path.dirname(os.path.abspath(__file__))
    routers_path = os.path.join(base_path, routers_dir)

    for root, _, files in os.walk(routers_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)
                
                # Convert file path to route path
                relative_path = os.path.relpath(file_path, routers_path)
                route_path = convert_path_to_route(relative_path)
                
                # Import the module
                module_path = get_module_path(file_path, base_path)
                module = importlib.import_module(module_path)
                
                # If module has router, include it
                if hasattr(module, 'router'):
                    prefix = f"/api/{route_path}"
                    main_router.include_router(module.router, prefix=prefix)

    return main_router 