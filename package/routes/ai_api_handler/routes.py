"""########################################################################################
Name: ai_api_handler/routes.py
Description: 
Imports:
"""

from typing import Annotated

from fastapi import APIRouter, Body, Header, Response

from ...utils.decorators import session_fetch
from ..session.models import *
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

        self.add_api_route(
            path="/text_to_speech",
            endpoint=self.text_to_speech,
            methods=["POST"],
        )

    ############################################################
    # getter functions:

    @session_fetch
    async def get_voices_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> List[str]:
        return session.api_engine_modules.ai_api_engine.get_voices(api_key=api_key)

    @session_fetch
    async def get_voice_settings_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        voice_id: Annotated[str, Header()] = None,
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> Voice_Settings:
        return session.api_engine_modules.ai_api_engine.get_voice_settings(
            api_key=api_key, voice_id=voice_id
        )

    ############################################################
    # setter functions:

    ############################################################
    # post functions:
    @session_fetch
    async def text_to_speech(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        data: Text_To_Speech,
        session: Optional[Session] = Body(None, include_in_schema=False),
    ) -> Response:
        try:
            file_in_bytes: bytes = (
                session.api_engine_modules.ai_api_engine.text_to_speech(
                    api_key=api_key,
                    text=data.text,
                    voice=data.voice,
                    voice_settings=data.voice_settings,
                    model=data.model,
                    seed=data.seed,
                    audio_format=session.session_settings.audio_format,
                )
            )

            media_type = f"audio/{session.session_settings.audio_format}"

            return Response(content=file_in_bytes, media_type=media_type)
        except Exception as e:
            return Response(content=f"Error: {e}", media_type="text/plain")

    ############################################################
    # put functions:

    ############################################################
    # delete functions:
