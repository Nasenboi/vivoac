"""########################################################################################
Name: user/routes.py
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
from .dependencies import *
from .functions import *
from .models import *

"""
########################################################################################"""


# create a new router
class User_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {"prefix": "/user", "tags": ["user"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine
        self.add_api_route(path="/add", endpoint=self.add_user_route, methods=["POST"])
        self.add_api_route(path="/get", endpoint=self.get_user_route, methods=["GET"])
        self.add_api_route(path="/self", endpoint=self.self_route, methods=["GET"])
        self.add_api_route(
            path="/update", endpoint=self.update_user_route, methods=["PUT"]
        )
        self.add_api_route(
            path="/delete", endpoint=self.delete_user_route, methods=["DELETE"]
        )

    async def add_user_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_to_add: UserForEdit,
    ) -> User:
        return await add_user(user_to_add)

    async def get_user_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_to_get: Annotated[User_Query, Depends()],
    ) -> Union[User, List[User]]:
        return await get_user(user_to_get)

    async def self_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency()),
        ],
    ) -> User:
        return vivoac_base_header.user

    async def update_user_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_id: str,
        user_to_edit: UserForEdit,
    ) -> User:
        return await update_user(user_id, user_to_edit)

    async def delete_user_route(
        self,
        vivoac_base_header: Annotated[
            VivoacBaseHeader,
            Depends(get_vivoac_base_header_dependency(check_admin=True)),
        ],
        user_id: str,
    ) -> User:
        return await delete_user(user_id)
