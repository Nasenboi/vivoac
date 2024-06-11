"""########################################################################################
Name: audio/routes.py
Description: 
Imports:
"""

import json
from typing import Annotated, Any, Dict

from fastapi import APIRouter, Body, Header

from ...globals import LOGGER
from .models import *

"""
########################################################################################"""


class Engine_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {
        "prefix": "/engine",
        "tags": ["engine"],
        "responses": {404: {"description": "Not found"}},
    }

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

        self.add_api_route(
            path="/get", endpoint=self.get_session_engines_route, methods=["GET"]
        )
        self.add_api_route(
            path="/update", endpoint=self.update_session_engines_route, methods=["POST"]
        )
        self.add_api_route(
            path="/settings/get",
            endpoint=self.get_engine_settings_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/settings/update",
            endpoint=self.update_engine_settings_route,
            methods=["POST"],
        )

    async def get_session_engines_route(
        self,
        session_id: Annotated[str, Header()],
    ) -> Engine_Modules:
        return await self.api_engine.engine_backend.get_session_engine_names(
            session_id=session_id
        )

    async def update_session_engines_route(
        self,
        session_id: Annotated[str, Header()],
        engine_modules: Engine_Modules,
    ) -> str | int:
        return await self.api_engine.engine_backend.update_session_engines(
            session_id=session_id, engine_modules=engine_modules
        )

    # == Engine Settings ==

    async def get_engine_settings_route(
        self,
        session_id: Annotated[str, Header()],
        engine_module_name: str,
    ) -> dict:
        return await self.api_engine.engine_backend.get_session_engine_settings(
            session_id=session_id, engine_module_name=engine_module_name
        )

    async def update_engine_settings_route(
        self,
        session_id: Annotated[str, Header()],
        engine_module_name: str,
        engine_settings: Annotated[Dict[str, Any], Body()],
    ) -> str | int:
        LOGGER.debug(f"Updating engine settings: {engine_settings}")
        return await self.api_engine.engine_backend.update_session_engine_settings(
            session_id=session_id,
            engine_module_name=engine_module_name,
            engine_settings=engine_settings,
        )
