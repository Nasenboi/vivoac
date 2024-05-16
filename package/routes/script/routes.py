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
script_router = APIRouter(
    prefix="/script",
    tags=["script"],
    responses={404: {"description": "Not found"}},
)


# complete a script model by the given parameters
@script_router.get("/{script}")
def get_script_route(script: Script) -> Union[List, Script, dict]:
    return get_script(script)
