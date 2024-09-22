"""########################################################################################
Name: script/routes.py
Description: 
Imports:
"""

from typing import Annotated, Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, Header, HTTPException

from ...globals import LOGGER, SETTINGS_GLOBAL
from ...http_models import (
    VivoacBaseHeader,
    VivoacBaseResponse,
    get_vivoac_base_header_dependency,
)
from ..user.dependencies import get_current_user
from ..user.models import User
from .functions import *
from .models import *

"""
########################################################################################"""


# create a new router
class Script_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {"prefix": "/script", "tags": ["script"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine
        self.add_api_route(
            path="/get",
            endpoint=self.get_script_lines_route,
            methods=["GET"],
        )

    async def get_script_lines_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency()),
        ],
        script_line: Annotated[Script_Line, Depends()],
    ) -> List[Script_Line]:
        LOGGER.debug(f"Getting script lines for {script_line}")
        script_db_engine = (
            self.api_engine.engine_backend.engine_modules.script_db_engine
        )
        script_lines = await get_script_lines(
            script_line=script_line, script_db_engine=script_db_engine
        )
        return script_lines
