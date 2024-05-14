'''########################################################################################
Name: script/routes.py
Description: 
Imports:
'''
from fastapi import APIRouter
from .models import *
from .functions import *
from ...globals import SETTINGS_GLOBAL, LOGGER
from typing import Union, List
'''
########################################################################################'''


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