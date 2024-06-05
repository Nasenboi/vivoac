"""########################################################################################
Name: script/routes.py
Description: 
Imports:
"""

from typing import Annotated, List, Optional, Union

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
            methods=["Post"],
        )

    @session_fetch
    async def get_script_lines_route(
        self,
        script_line: Script_Line,
        session_id: Annotated[str, Header()],
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> Union[List[Script_Line | dict], Script_Line, dict]:
        LOGGER.debug(f"Getting script lines for {script_line}")
        return await get_script_lines(script_line=script_line, session=session)
