"""########################################################################################
Name: user/routes.py
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
from ...utils.models import PydanticObjectId
from .dependencies import *
from .functions import *
from .models import *

"""
########################################################################################"""


# create a new router
class User_Router(APIRouter):
    api_engine: API_Engine_Base = None
    route_parameters: dict = {"prefix": "/user", "tags": ["user"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine
        self.add_api_route(path="/", endpoint=self.add_user_route, methods=["POST"])
        self.add_api_route(
            methods=["GET"],
            path="/{user_id}",
            endpoint=self.get_user_route,
        )
        self.add_api_route(methods=["GET"], path="/", endpoint=self.find_users_route)
        self.add_api_route(path="/whoami", endpoint=self.self_route, methods=["GET"])
        self.add_api_route(
            path="/{user_id}", endpoint=self.update_user_route, methods=["PUT"]
        )
        self.add_api_route(
            path="/{user_id}", endpoint=self.delete_user_route, methods=["DELETE"]
        )

    async def add_user_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_to_add: UserForEdit,
    ) -> VivoacBaseResponse[User]:
        return VivoacBaseResponse(data=await create_user(user_to_add))

    async def get_user_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_id: PydanticObjectId,
    ) -> VivoacBaseResponse[User]:
        return VivoacBaseResponse(data=await get_user(user_id=user_id))

    async def find_users_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_query: Annotated[User_Query, Depends()],
    ) -> VivoacBaseResponse[List[User]]:
        return VivoacBaseResponse(
            data=await find_users(
                user_query=user_query.model_dump(exclude_unset=True),
            )
        )

    async def self_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency()),
        ],
    ) -> VivoacBaseResponse[User]:
        return VivoacBaseResponse(data=vivoac_base_header.user)

    async def update_user_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_id: PydanticObjectId,
        user_to_edit: UserForEdit,
    ) -> VivoacBaseResponse[User]:
        return VivoacBaseResponse(data=await update_user(user_id, user_to_edit))

    async def delete_user_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_id: PydanticObjectId,
    ) -> VivoacBaseResponse[User]:
        return VivoacBaseResponse(data=await delete_user(user_id))
