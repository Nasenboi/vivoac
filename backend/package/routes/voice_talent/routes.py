"""########################################################################################
Name: voice_talent/routes.py
Description: 
Imports:
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends

from .functions import *
from .models import *

"""
########################################################################################"""


# create a new router
class Voice_Talent_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {
        "prefix": "/voice_talent",
        "tags": ["voice_talent"],
        "responses": {404: {"description": "Not found"}},
    }

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine
