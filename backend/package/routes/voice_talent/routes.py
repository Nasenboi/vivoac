"""########################################################################################
Name: voice_talent/routes.py
Description: 
Imports:
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends

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
class Voice_Talent_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {"prefix": "/voice_talent", "tags": ["voice_talent"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

        self.add_api_route(
            methods=["GET"],
            path="/{voice_talent_id}",
            endpoint=self.get_voice_talent_route,
        )
        self.add_api_route(
            methods=["GET"], path="/", endpoint=self.find_voice_talents_route
        )
        self.add_api_route(
            methods=["POST"],
            path="/",
            endpoint=self.create_voice_talent_route,
        )
        self.add_api_route(
            methods=["PUT"],
            path="/{voice_talent_id}",
            endpoint=self.update_voice_talent_route,
        )
        self.add_api_route(
            methods=["DELETE"],
            path="/{voice_talent_id}",
            endpoint=self.delete_voice_talent_route,
        )

    # -- Get --
    async def get_voice_talent_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_talent_id: PydanticObjectId,
    ) -> VivoacBaseResponse[Voice_Talent]:
        return VivoacBaseResponse[Voice_Talent](
            data=await get_voice_talent(voice_talent_id=voice_talent_id)
        )

    async def find_voice_talents_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_talent_query: Voice_Talent = Depends()
    ) -> VivoacBaseResponse[List[Voice_Talent]]:
        return VivoacBaseResponse[List[Voice_Talent]](
            data=await find_voice_talents(
                voice_talent_query=voice_talent_query.model_dump(),
            )
        )

    # -- Post --
    async def create_voice_talent_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_talent: Voice_Talent,
    ) -> VivoacBaseResponse[Voice_Talent]:
        return VivoacBaseResponse[Voice_Talent](
            data=await create_voice_talent(voice_talent=voice_talent)
        )

    # -- Put --
    async def update_voice_talent_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_talent_id: str,
        voice_talent: Voice_Talent,
    ) -> VivoacBaseResponse[Voice_Talent]:
        return VivoacBaseResponse[Voice_Talent](
            data=await update_voice_talent(
                voice_talent_id=voice_talent_id, voice_talent=voice_talent
            )
        )

    # -- Delete --
    async def delete_voice_talent_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader, Depends(get_vivoac_base_header_dependency())
        ],
        voice_talent_id: PydanticObjectId,
    ) -> VivoacBaseResponse[Voice_Talent]:
        return VivoacBaseResponse[Voice_Talent](
            data=await delete_voice_talent(voice_talent_id=voice_talent_id)
        )
