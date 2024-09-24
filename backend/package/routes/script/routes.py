"""########################################################################################
Name: script/routes.py
Description: 
Imports:
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends

from ...api_engine.api_engine_base import API_Engine_Base
from ...globals import LOGGER
from ...http_models import (
    VivoacBaseHeader,
    VivoacBaseResponse,
    get_vivoac_base_header_dependency,
)
from .functions import *
from .models import *

"""
########################################################################################"""


# create a new router
class Script_Router(APIRouter):
    api_engine: API_Engine_Base = None
    route_parameters: dict = {"prefix": "/script", "tags": ["script"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine
        self.add_api_route(
            path="/find",
            endpoint=self.find_script_lines_route,
            methods=["GET"],
        )

    async def find_script_lines_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency()),
        ],
        script_line: Annotated[Script_Line, Depends()],
    ) -> VivoacBaseResponse[List[Script_Line]]:
        LOGGER.debug(f"Getting script lines for {script_line}")
        VivoacBaseResponse(
            data=await self.api_engine.script_db_engine.find_script_lines(script_line)
        )
