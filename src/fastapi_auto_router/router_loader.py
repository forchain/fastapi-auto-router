import importlib
import os
import sys
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter, FastAPI

class AutoRouter:
    """
    Automatic router configuration based on filesystem structure
    """
    def __init__(
        self,
        app: FastAPI,
        routers_dir: str,
        api_prefix: str = "/api",
        base_path: Optional[str] = None
    ):
        """
        Initialize AutoRouter
        
        Args:
            app: FastAPI application instance
            routers_dir: Directory containing router files
            api_prefix: Prefix for all API routes (default: "/api")
            base_path: Base path for router files (default: current working directory)
        """
        self.app = app
        self.routers_dir = routers_dir
        self.api_prefix = api_prefix.rstrip('/')
        self.base_path = base_path or os.getcwd()
        self.main_router = APIRouter()

    def _convert_path_to_route(self, path: str) -> str:
        """Convert filesystem path to API route path"""
        if path.endswith('/__init__.py'):
            path = path[:-12]
        elif path.endswith('.py'):
            path = path[:-3]
        parts = path.split('/')
        converted_parts = []
        for part in parts:
            if part.startswith('{') and part.endswith('}'):
                converted_parts.append(part)
            else:
                converted_parts.append(part.replace('_', '-'))
        return '/'.join(converted_parts)

    def _get_module_path(self, file_path: str, routers_path: str) -> str:
        """Convert file path to module import path"""
        # Get the relative path to the routers directory
        relative_path = os.path.relpath(file_path, routers_path)
        # Remove the .py extension
        if relative_path.endswith('.py'):
            relative_path = relative_path[:-3]
        # Convert path separators to dots
        return relative_path.replace('/', '.').replace('\\', '.')

    def load_routers(self) -> None:
        """Load all routers from the specified directory"""
        # Resolve routers_path: use base_path if routers_dir is relative
        if os.path.isabs(self.routers_dir):
            routers_path = os.path.abspath(self.routers_dir)
        else:
            routers_path = os.path.abspath(os.path.join(self.base_path, self.routers_dir))
        
        sys.path.insert(0, routers_path)

        try:
            for root, _, files in os.walk(routers_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        
                        # Convert file path to route path
                        relative_path = os.path.relpath(file_path, routers_path)
                        route_path = self._convert_path_to_route(relative_path)
                        
                        # Import the module
                        module_path = f"{self._get_module_path(file_path, routers_path)}"
                        module = importlib.import_module(module_path)
                        
                        # If module has router, include it
                        if hasattr(module, 'router'):
                            prefix = f"{self.api_prefix}/{route_path}"
                            self.main_router.include_router(module.router, prefix=prefix)

        finally:
            # Clean up sys.path
            sys.path.pop(0)

        # Include the main router in the FastAPI app
        self.app.include_router(self.main_router) 