"""########################################################################################
Name: ai_api_handler/routes.py
Description: 
Imports:
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response

from ...http_models import (
    VivoacBaseHeader,
    VivoacBaseResponse,
    get_vivoac_base_header_dependency,
)
from .models import *

"""
########################################################################################"""


class AI_API_Handler_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {"prefix": "/ai_api_handler", "tags": ["ai_api_handler"]}

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
            path="/delete_voice/{voice_id}",
            endpoint=self.delete_voice_route,
            methods=["DELETE"],
        )

    ############################################################
    # getter functions:

    async def get_user_data_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(get_api_key=True)),
        ],
    ) -> dict:
        return self.api_engine.engine_backend.engine_modules.get_user_data(
            api_key=vivoac_base_header.api_key
        )

    async def get_models_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(get_api_key=True)),
        ],
    ) -> dict:
        return self.api_engine.engine_backend.engine_modules.ai_api_engine.get_models(
            api_key=vivoac_base_header.api_key
        )

    async def get_voices_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(get_api_key=True)),
        ],
    ) -> List[str]:
        return self.api_engine.engine_backend.engine_modules.ai_api_engine.get_voices(
            api_key=vivoac_base_header.api_key
        )

    async def get_voice_settings_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(get_api_key=True)),
        ],
        voice_id: str = Query(),
        name: str = Query(),
    ) -> Voice_Settings:
        return self.api_engine.engine_backend.engine_modules.ai_api_engine.get_voice_settings(
            api_key=vivoac_base_header.api_key, voice_id=voice_id, name=name
        )

    ############################################################
    # put functions:

    async def create_voice_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(get_api_key=True)),
        ],
        voice_settings: Voice_Settings,
    ) -> str:
        return self.api_engine.engine_backend.engine_modules.ai_api_engine.create_voice(
            api_key=vivoac_base_header.api_key,
            voice_settings=voice_settings,
        )

    ############################################################

    async def edit_voice_settings_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(get_api_key=True)),
        ],
        voice_settings: Voice_Settings,
    ) -> None:
        return self.api_engine.engine_backend.engine_modules.ai_api_engine.edit_voice_settings(
            api_key=vivoac_base_header.api_key,
            voice_settings=voice_settings,
        )

    # post functions:
    async def text_to_speech(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(get_api_key=True)),
        ],
        data: Text_To_Speech,
    ) -> Response:
        try:
            file_in_bytes: bytes = (
                self.api_engine.engine_backend.engine_modules.ai_api_engine.text_to_speech(
                    api_key=vivoac_base_header.api_key,
                    text=data.text,
                    voice=data.voice,
                    voice_settings=data.voice_settings,
                    model=data.model,
                    seed=data.seed,
                    audio_format=vivoac_base_header.user.config.audio_format,
                )
            )
            # TODO: MIME Type mapper
            media_type = f"audio/{vivoac_base_header.user.config.audio_format.codec}"

            return Response(content=file_in_bytes, media_type=media_type)
        except Exception as e:
            return Response(content=f"Error: {e}", media_type="text/plain")

    ############################################################
    # delete functions:
    async def delete_voice_route(
        self,
        voice_id: str,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(get_api_key=True)),
        ],
    ) -> None:
        return self.api_engine.engine_backend.engine_modules.ai_api_engine.delete_voice(
            api_key=vivoac_base_header.api_key, voice_id=voice_id, name=None
        )
