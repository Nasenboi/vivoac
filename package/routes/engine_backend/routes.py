"""########################################################################################
Name: audio/routes.py
Description: 
Imports:
"""

from typing import Annotated, Any, Dict

from fastapi import APIRouter, Body, Header

from ...globals import LOGGER
from ...utils.decorators import session_fetch
from ..session.models import Session
from .models import *

"""
########################################################################################"""


class Engine_Router(APIRouter):
    session_engine = None
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
            path="/update", endpoint=self.update_session_engines_route, methods=["PUT"]
        )
        self.add_api_route(
            path="/settings/get",
            endpoint=self.get_engine_settings_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/settings/update",
            endpoint=self.update_engine_settings_route,
            methods=["PUT"],
        )

    @session_fetch
    async def get_session_engines_route(
        self,
        session_id: Annotated[str, Header()],
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> Engine_Modules:
        return await self.session_engine.engine_backend.get_session_engine_names(
            session=session
        )

    @session_fetch
    async def update_session_engines_route(
        self,
        session_id: Annotated[str, Header()],
        engine_modules: Engine_Modules,
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> str | int:
        LOGGER.debug(f"Updating session engines: {engine_modules}")
        result = await self.session_engine.engine_backend.update_session_engines(
            session=session, engine_modules=engine_modules
        )
        await self.api_engine.session_backend.update(
            session_id=session_id, data=session
        )
        return result

    # == Engine Settings ==
    @session_fetch
    async def get_engine_settings_route(
        self,
        session_id: Annotated[str, Header()],
        engine_module_name: str,
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> dict:
        return await self.session_engine.engine_backend.get_session_engine_settings(
            session=session, engine_module_name=engine_module_name
        )

    @session_fetch
    async def update_engine_settings_route(
        self,
        session_id: Annotated[str, Header()],
        engine_module_name: str,
        engine_settings: Annotated[dict, Body()],
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> str | int:
        LOGGER.debug(f"Updating engine settings: {engine_settings}")
        result = (
            await self.session_engine.engine_backend.update_session_engine_settings(
                session=session,
                engine_module_name=engine_module_name,
                engine_settings=engine_settings,
            )
        )
        await self.api_engine.session_backend.update(
            session_id=session_id, data=session
        )
        return result
