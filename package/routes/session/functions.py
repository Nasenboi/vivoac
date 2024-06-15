"""########################################################################################
Name: session/functions.py
Description: 
Imports:
"""

from ...globals import LOGGER
from .models import Session

"""
########################################################################################"""


async def create_session(self, api_engine, session: Session) -> Session:
    session.fill_default_values()
    LOGGER.debug(f"Creating session: {session.session_id}")
    await self.engine_backend.add_session_engines(session=session)
    await api_engine.session_backend.create(session_id=session.session_id, data=session)
    return session


async def close_session(self, api_engine, session_id: str | int) -> Session:
    LOGGER.debug(f"Closing session: {session_id}")
    await api_engine.session_backend.delete(session_id)
    return session_id


async def get_session(api_engine, session_id: str | int) -> Session:
    LOGGER.debug(f"Fetching session: {session_id}")
    session = await api_engine.session_backend.read(session_id=session_id)
    return session


async def update_session(
    api_engine, session_id: str | int, new_session: Session, session: Session
) -> Session:
    LOGGER.debug(f"Updating session: {session_id}")
    if session.session_id is not None and session_id != session.session_id:
        raise ValueError(f"Session ID mismatch: {session_id} != {session.session_id}")

    session.update(new_session)

    await api_engine.session_backend.update(session_id=session_id, data=session)
    return session
