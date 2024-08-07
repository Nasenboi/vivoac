"""########################################################################################
Name: ai_api_handler/routes.py
Description: 
Imports:
"""

from typing import Annotated

from fastapi import APIRouter, Body, Header, Response

from ...utils.functions import fetch_session
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
            path="/get_user_data",
            endpoint=self.get_user_data_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/get_models",
            endpoint=self.get_models_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/get_voices",
            endpoint=self.get_voices_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/get_voice_settings",
            endpoint=self.get_voice_settings_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/create_voice",
            endpoint=self.create_voice_route,
            methods=["POST"],
        )
        self.add_api_route(
            path="/update_voice_settings",
            endpoint=self.edit_voice_settings_route,
            methods=["PUT"],
        )
        self.add_api_route(
            path="/text_to_speech",
            endpoint=self.text_to_speech,
            methods=["POST"],
        )
        self.add_api_route(
            path="/delete_voice",
            endpoint=self.delete_voice_route,
            methods=["DELETE"],
        )

    ############################################################
    # getter functions:

    async def get_user_data_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
    ) -> dict:
        session = await fetch_session(self.api_engine, session_id)
        return session.api_engine_modules.ai_api_engine.get_user_data(api_key=api_key)

    async def get_models_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
    ) -> dict:
        session = await fetch_session(self.api_engine, session_id)
        return session.api_engine_modules.ai_api_engine.get_models(api_key=api_key)

    async def get_voices_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
    ) -> List[str]:
        session = await fetch_session(self.api_engine, session_id)
        return session.api_engine_modules.ai_api_engine.get_voices(api_key=api_key)

    async def get_voice_settings_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        voice_id: Annotated[str, Header()] = None,
        name: Annotated[str, Header()] = None,
    ) -> Voice_Settings:
        session = await fetch_session(self.api_engine, session_id)
        return session.api_engine_modules.ai_api_engine.get_voice_settings(
            api_key=api_key, voice_id=voice_id, name=name
        )

    ############################################################
    # put functions:

    async def create_voice_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        voice_settings: Voice_Settings,
    ) -> str:
        session = await fetch_session(self.api_engine, session_id)
        return session.api_engine_modules.ai_api_engine.create_voice(
            api_key=api_key,
            voice_settings=voice_settings,
        )

    ############################################################

    async def edit_voice_settings_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        voice_settings: Voice_Settings,
    ) -> None:
        session = await fetch_session(self.api_engine, session_id)
        return session.api_engine_modules.ai_api_engine.edit_voice_settings(
            api_key=api_key,
            voice_settings=voice_settings,
        )

    # post functions:
    async def text_to_speech(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        data: Text_To_Speech,
    ) -> Response:
        session = await fetch_session(self.api_engine, session_id)
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
    # delete functions:
    async def delete_voice_route(
        self,
        session_id: Annotated[str, Header()],
        api_key: Annotated[str, Header()],
        voice_id: Annotated[str, Header()],
    ) -> None:
        session = await fetch_session(self.api_engine, session_id)
        return session.api_engine_modules.ai_api_engine.delete_voice(
            api_key=api_key, voice_id=voice_id, name=None
        )
