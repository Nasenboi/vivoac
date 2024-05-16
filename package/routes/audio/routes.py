"""########################################################################################
Name: audio/routes.py
Description: 
Imports:
"""

from fastapi import APIRouter

"""
########################################################################################"""


class Audio_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {
        "prefix": "/audio",
        "tags": ["audio"],
        "responses": {404: {"description": "Not found"}},
    }

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine
