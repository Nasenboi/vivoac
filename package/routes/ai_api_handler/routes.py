"""########################################################################################
Name: ai_api_handler/routes.py
Description: 
Imports:
"""

from typing import Annotated

from fastapi import APIRouter, Header

from ...utils.decorators import session_fetch
from .models import *

"""
########################################################################################"""


class AI_API_Handler_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {
        "prefix": "/ai_api_handler",
        "tags": ["ai_api_handler"],
        "responses": {404: {"description": "Not found"}},
    }

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

    ############################################################
    # getter functions:

    @session_fetch
    async def text_to_speech(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        data: TextToSpeech,
    ):
        return await self.api_engine.text_to_speech(text=text, session_id=session_id)

    ############################################################
    # setter functions:

    ############################################################
    # post functions:

    ############################################################
    # put functions:

    ############################################################
    # delete functions:
