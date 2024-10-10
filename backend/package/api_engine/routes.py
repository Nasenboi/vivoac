"""########################################################################################
Name: api_engine/routes.py
Description: 
Imports:
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from ..auth import authenticate_user, create_access_token

from ..routes.user.models import Token, TokenData

"""
########################################################################################"""


class API_Engine_Router(APIRouter):
    api_engine = None
    route_parameters: dict = {"prefix": "", "tags": ["api_engine"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

        self.add_api_route(path="/token", endpoint=self.token_route, methods=["POST"])

    async def token_route(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            TokenData(username=user.username, id=str(user.id))
        )
        return Token(access_token=access_token, token_type="bearer")
