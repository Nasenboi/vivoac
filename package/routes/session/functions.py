"""########################################################################################
Name: session/functions.py
Description: 
Imports:
"""

from ...globals import LOGGER
from .models import Session

"""
########################################################################################"""


async def create_session(api_engine, session: Session) -> Session:
    LOGGER.debug(f"Creating session: {session.session_id}")
    await api_engine.session_backend.create(session_id=session.session_id, data=session)
    api_engine.engine_backend.add_session_engines(session_id=session.session_id)
    return session


async def close_session(api_engine, session: Session) -> Session:
    LOGGER.debug(f"Closing session: {session.session_id}")
    await api_engine.session_backend.delete(session.session_id)
    return session


async def get_session(api_engine, session_id: str | int) -> Session:
    LOGGER.debug(f"Fetching session: {session_id}")
    session = await api_engine.session_backend.read(session_id=session_id)
    return session


async def update_session(api_engine, session: Session) -> Session:
    LOGGER.debug(f"Updating session: {session.session_id}")
    await api_engine.session_backend.update(session_id=session.session_id, data=session)
    return session
