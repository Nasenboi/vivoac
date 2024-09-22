"""########################################################################################
Name: audio/routes.py
Description: 
Imports:
"""

from typing import Annotated, Any, Dict, Union

from fastapi import APIRouter, Body, Depends, Header

from ...globals import LOGGER
from ...http_models import (
    VivoacBaseHeader,
    VivoacBaseResponse,
    get_vivoac_base_header_dependency,
)
from .models import *

"""
########################################################################################"""


class Engine_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {"prefix": "/engine", "tags": ["engine"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

        self.add_api_route(
            path="/get", endpoint=self.get_engines_route, methods=["GET"]
        )
        self.add_api_route(
            path="/set", endpoint=self.set_engines_route, methods=["PUT"]
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

    async def get_engines_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
    ) -> Dict[str, str]:
        return {
            "ai_api_engine": await self.api_engine.engine_backend.get_ai_api_engine_name(),
            "script_db_engine": await self.api_engine.engine_backend.get_script_db_engine_name(),
        }

    async def set_engines_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        ai_api_engine_module: AI_API_ENGINE_MODULE_KEYS = Body(),
        script_db_engine_module: SCRIPT_DB_ENGINE_MODULE_KEYS = Body(),
    ) -> Union[str, int]:
        LOGGER.debug(
            f"Updating engines: {ai_api_engine_module}, {script_db_engine_module}"
        )
        result = await self.api_engine.engine_backend.set_engine_module(
            ai_api_engine_module=ai_api_engine_module,
            script_db_engine_module=script_db_engine_module,
        )
        return result

    # == Engine Settings ==
    async def get_engine_settings_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency()),
        ],
    ) -> Dict[str, dict]:
        return {
            "ai_api_engine": await self.api_engine.engine_backend.get_ai_api_engine_settings(),
            "script_db_engine": await self.api_engine.engine_backend.get_script_db_engine_settings(),
        }

    async def update_engine_settings_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        ai_api_engine_settings: Optional[Dict[str, Any]] = None,
        script_db_engine_settings: Optional[Dict[str, Any]] = None,
    ) -> Union[str, int]:
        LOGGER.debug(f"Updating engine settings.")
        return await self.api_engine.engine_backend.update_engine_module_settings(
            ai_api_engine_settings=ai_api_engine_settings,
            script_db_engine_settings=script_db_engine_settings,
        )
