"""########################################################################################
Name: user/routes.py
Description: 
Imports:
"""

from fastapi import APIRouter

from .functions import *
from .models import *

"""
########################################################################################"""


# create a new router
class User_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {
        "prefix": "/user",
        "tags": ["user"],
        "responses": {404: {"description": "Not found"}},
    }

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine
        self.add_api_route(path="/add", endpoint=self.add_user_route, methods=["POST"])
        self.add_api_route(path="/get", endpoint=self.get_user_route, methods=["GET"])
        self.add_api_route(
            path="/update", endpoint=self.update_user_route, methods=["PUT"]
        )
        self.add_api_route(
            path="/delete", endpoint=self.delete_user_route, methods=["DELETE"]
        )

    async def add_user_route(self, user: UserForEdit) -> User:
        return await add_user(user)

    async def get_user_route(self, user_id: str) -> User:
        return await get_user(user_id)

    async def update_user_route(self, user_id: str, user: UserForEdit) -> User:
        return await update_user(user_id, user)

    async def delete_user_route(self, user_id: str) -> User:
        return await delete_user(user_id)
