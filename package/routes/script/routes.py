"""########################################################################################
Name: script/routes.py
Description: 
Imports:
"""

from typing import Annotated, Any, Dict, List, Optional, Union

from fastapi import APIRouter, Body, Header

from ...globals import LOGGER, SETTINGS_GLOBAL
from ...utils.decorators import session_fetch
from ..session.models import Session
from .functions import *
from .models import *

"""
########################################################################################"""


# create a new router
class Script_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {
        "prefix": "/script",
        "tags": ["script"],
        "responses": {404: {"description": "Not found"}},
    }

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine
        self.add_api_route(
            path="/get",
            endpoint=self.get_script_lines_route,
            methods=["GET"],
        )

    @session_fetch
    async def get_script_lines_route(
        self,
        session_id: Annotated[str, Header()],
        script_line: Optional[Script_Line] = Body(None, include_in_schema=False),
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> Union[List, Script_Line, Dict[str, Any]]:
        LOGGER.debug(f"Getting script lines for {script_line}")
        engines = await self.api_engine.engine_backend.get_session_engines(session_id)
        script_db_engine = engines.script_db_engine
        script_lines = await get_script_lines(
            script_line=script_line, script_db_engine=script_db_engine
        )
        return script_lines
