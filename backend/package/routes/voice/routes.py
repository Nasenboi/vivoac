"""########################################################################################
Name: voice/routes.py
Description: 
Imports:
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends

from ...api_engine.api_engine_base import API_Engine_Base
from ...http_models import (
    VivoacBaseHeader,
    VivoacBaseResponse,
    get_vivoac_base_header_dependency,
)
from .functions import *
from .models import *

"""
########################################################################################"""


# create a new router
class Voice_Router(APIRouter):
    api_engine: API_Engine_Base = None
    route_parameters: dict = {"prefix": "/voice", "tags": ["voice"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

        self.add_api_route(
            methods=["POST"],
            path="/crud",
            endpoint=self.create_voice_route,
        )
        self.add_api_route(
            methods=["GET"],
            path="/crud/{voice_id}",
            endpoint=self.get_voice_route,
        )
        self.add_api_route(
            methods=["PUT"],
            path="/crud/{voice_id}",
            endpoint=self.update_voice_route,
        )
        self.add_api_route(
            methods=["DELETE"],
            path="/crud/{voice_id}",
            endpoint=self.delete_voice_route,
        )
        self.add_api_route(
            methods=["GET"], path="/find", endpoint=self.find_voices_route
        )

    # -- Get --
    async def get_voice_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_id: PydanticObjectId,
    ) -> VivoacBaseResponse[Voice]:
        return VivoacBaseResponse(data=await get_voice(voice_id=voice_id))

    async def find_voices_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_query: Annotated[Voice_Query, Depends()],
    ) -> VivoacBaseResponse[List[Voice]]:
        return VivoacBaseResponse(
            data=await find_voices(
                voice_query=voice_query.model_dump(exclude_unset=True),
            )
        )

    # -- Post --
    async def create_voice_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice: Voice,
    ) -> VivoacBaseResponse[Voice]:
        return VivoacBaseResponse(data=await create_voice(voice=voice))

    # -- Put --
    async def update_voice_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_id: PydanticObjectId,
        voice: Voice,
    ) -> VivoacBaseResponse[Voice]:
        return VivoacBaseResponse(
            data=await update_voice(voice_id=voice_id, voice=voice)
        )

    # -- Delete --
    async def delete_voice_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_id: PydanticObjectId,
    ) -> VivoacBaseResponse[Voice]:
        return VivoacBaseResponse(data=await delete_voice(voice_id=voice_id))
