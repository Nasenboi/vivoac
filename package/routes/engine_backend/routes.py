"""########################################################################################
Name: audio/routes.py
Description: 
Imports:
"""

from typing import Annotated

from fastapi import APIRouter, Header

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

    async def get_session_engines_route(
        self,
        session_id: Annotated[str, Header()],
    ) -> API_Sub_Engines:
        return await self.api_engine.engine_backend.get_session_engines(
            session_id=session_id
        )

    async def update_session_engines_route(
        self,
        session_id: Annotated[str, Header()],
        engine_modules: Engine_Modules = Engine_Modules(),
    ) -> str | int:
        return await self.api_engine.engine_backend.update_session_engines(
            session_id=session_id, engine_modules=engine_modules
        )
