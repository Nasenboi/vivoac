"""########################################################################################
Name: script/routes.py
Description: 
Imports:
"""

from typing import List, Union

from fastapi import APIRouter

from ...globals import LOGGER, SETTINGS_GLOBAL
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
            path="/", endpoint=self.get_script_lines_route, methods=["GET"]
        )

    @staticmethod
    def get_script_lines_route(script: Script) -> Union[List, Script, dict]:
        # <call function from myApiEngine>
        return get_script_lines(script)
