"""########################################################################################
Name: session/routes.py
Description: 
Imports:
"""

from typing import Annotated

from fastapi import APIRouter, Body, Header

from ...utils.functions import fetch_session
from .functions import *
from .models import *

"""
########################################################################################"""


class Session_Router(APIRouter):
    api_engine = None
    engine_backend = None
    route_parameters: dict = {
        "prefix": "/session",
        "tags": ["session"],
        "responses": {404: {"description": "Not found"}},
    }

    def __init__(self, api_engine, **kwargs):
        self.route_parameters.update(kwargs)
        super().__init__(**self.route_parameters)
        self.api_engine = api_engine

        self.add_api_route(
            path="/create",
            endpoint=self.create_session_route,
            methods=["POST"],
            description="""
                        Create a new session for this api.
                        You can pass known session settings as input and let the api fill out the rest.

                        **Inputs**:
                            - Body: **session**: the optional session settings, inkl. session_id, engines and settings.\f

                        **Returns**:
                            - **session**: the created session settings, inkl. session_id, engines and settings.
                    """,
        )
        self.add_api_route(
            path="/close", endpoint=self.close_session_route, methods=["POST"]
        )
        self.add_api_route(
            path="/get", endpoint=self.get_session_route, methods=["GET"]
        )
        self.add_api_route(
            path="/update", endpoint=self.update_session_route, methods=["POST"]
        )

    async def create_session_route(
        self,
        session: Optional[Session] = Session(),
    ) -> Session:
        return await create_session(
            self=self, api_engine=self.api_engine, session=session
        )

    async def close_session_route(
        self,
        session_id: Annotated[str, Header()],
    ) -> str | int:
        return await close_session(
            self=self, api_engine=self.api_engine, session_id=session_id
        )

    async def get_session_route(
        self,
        session_id: Annotated[str, Header()],
    ) -> Session:
        session_fetched, session = fetch_session(self.api_engine, session_id)
        if not session_fetched:
            return {"error": "Failed to fetch session."}
        return session

    async def update_session_route(
        self,
        session_id: Annotated[str, Header()],
        new_session: Session,
    ) -> Session:
        session_fetched, session = fetch_session(self.api_engine, session_id)
        if not session_fetched:
            return {"error": "Failed to fetch session."}
        return await update_session(
            api_engine=self.api_engine,
            session_id=session_id,
            new_session=new_session,
            session=session,
        )
