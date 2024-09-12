"""########################################################################################
Name: session/routes.py
Description: 
Imports:
"""

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException

from ...utils.functions import fetch_session
from .functions import *
from .models import *

from ...http_models import (
    VivoacBaseHeader,
    VivoacBaseResponse,
    get_vivoac_base_header_dependency,
)

"""
########################################################################################"""


class Session_Router(APIRouter):
    api_engine = None
    engine_backend = None
    route_parameters: dict = {"prefix": "/session", "tags": ["session"]}

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

        self.add_api_route(
            path="/create",
            endpoint=self.create_session_route,
            methods=["POST"],
        )
        self.add_api_route(
            path="/get/{path_session_id}",
            endpoint=self.get_session_route,
            methods=["GET"],
        )
        self.add_api_route(
            path="/update/{path_session_id}",
            endpoint=self.update_session_route,
            methods=["PUT"],
        )
        self.add_api_route(
            path="/close/{path_session_id}",
            endpoint=self.close_session_route,
            methods=["DELETE"],
        )

    async def create_session_route(
        self, session: Optional[Session] = None
    ) -> VivoacBaseResponse[Session]:
        session = await create_session(
            self=self, api_engine=self.api_engine, session=session
        )
        return VivoacBaseResponse[Session](session_id=session.session_id, data=session)

    async def get_session_route(
        self,
        path_session_id: str,
        session_id: Annotated[str, Header()],
    ) -> Session:
        if session_id != path_session_id:
            raise HTTPException(
                status_code=403, detail="You are not allowed to access this session!"
            )
        session = await fetch_session(self.api_engine, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found!")
        return session

    async def update_session_route(
        self,
        path_session_id: str,
        session_id: Annotated[str, Header()],
        new_session: Session,
    ) -> Session:
        if session_id != path_session_id:
            raise HTTPException(
                status_code=403, detail="You are not allowed to edit this session!"
            )
        session = await fetch_session(self.api_engine, session_id)
        return await update_session(
            api_engine=self.api_engine,
            session_id=session_id,
            new_session=new_session,
            session=session,
        )

    async def close_session_route(
        self, path_session_id: str, session_id: Annotated[str, Header()]
    ) -> Union[str, int]:
        if session_id != path_session_id:
            raise HTTPException(
                status_code=403, detail="You are not allowed to close this session!"
            )
        return await close_session(
            self=self, api_engine=self.api_engine, session_id=session_id
        )
