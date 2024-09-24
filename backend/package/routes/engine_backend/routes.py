"""########################################################################################
Name: audio/routes.py
Description: 
Imports:
"""

from typing import Annotated, Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends

from ...api_engine.api_engine_base import API_Engine_Base
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
    api_engine: API_Engine_Base = None
    route_parameters: dict = {"prefix": "/engine", "tags": ["engine"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

        self.add_api_route(
            path="/names", endpoint=self.get_engine_names_route, methods=["GET"]
        )
        self.add_api_route(
            path="/get_modules/{engine_type}",
            endpoint=self.get_modules_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/set/{engine_type}", endpoint=self.set_engine_route, methods=["PUT"]
        )
        self.add_api_route(
            path="/settings/{engine_type}/get",
            endpoint=self.get_engine_settings_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/settings/{engine_type}/update",
            endpoint=self.update_engine_settings_route,
            methods=["PUT"],
        )

    async def get_engine_names_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
    ) -> VivoacBaseResponse[Dict[str, str]]:
        data = {
            "ai_api_engine": await self.api_engine.engine_backend.get_ai_api_engine_name(),
            "script_db_engine": await self.api_engine.engine_backend.get_script_db_engine_name(),
        }
        return VivoacBaseResponse(data=data)

    async def get_modules_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        engine_type: ENGINE_TYPES,
    ) -> VivoacBaseResponse[List[str]]:
        if engine_type == "ai_api_engine":
            modules = list(ai_api_engine_modules.keys())
        elif engine_type == "script_db_engine":
            modules = list(script_db_engine_modules.keys())
        return VivoacBaseResponse(data=modules)

    async def set_engine_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        engine_type: ENGINE_TYPES,
        module: Union[AI_API_ENGINE_MODULE_KEYS, SCRIPT_DB_ENGINE_MODULE_KEYS] = Body(),
    ) -> VivoacBaseResponse[Dict[str, str]]:
        LOGGER.debug(f"Updating engine: {engine_type} with module: {module}.")
        return VivoacBaseResponse(
            data=await self.api_engine.engine_backend.set_engine_module(
                engine_type=engine_type, module=module
            )
        )

    # == Engine Settings ==
    async def get_engine_settings_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency()),
        ],
        engine_type: ENGINE_TYPES,
    ) -> VivoacBaseResponse[dict]:
        if engine_type == "ai_api_engine":
            data = await self.api_engine.engine_backend.get_ai_api_engine_settings()
        elif engine_type == "script_db_engine":
            data = await self.api_engine.engine_backend.get_script_db_engine_settings()
        return VivoacBaseResponse(data=data)

    async def update_engine_settings_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        engine_type: ENGINE_TYPES,
        settings: Optional[Dict[str, Any]] = None,
    ) -> VivoacBaseResponse[Dict[str, Dict[str, Any]]]:
        LOGGER.debug(f"Updating engine settings.")
        data = await self.api_engine.engine_backend.update_engine_module_settings(
            engine_type=engine_type, settings=settings
        )
        return VivoacBaseResponse(data=data)
