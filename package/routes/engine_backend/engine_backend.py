"""########################################################################################
Name: engine_backend/engine_backend.py
Description: 
Imports:
"""

from typing import Any, Dict, List, Optional, Union

from ...globals import LOGGER
from ..session.models import Session
from .models import *

"""
########################################################################################"""


class Engine_Backend:
    async def add_session_engines(
        self,
        session: Session,
        engine_modules: Optional[
            Engine_Modules
        ] = Engine_Modules().fill_default_values(),
    ):
        session.api_engine_modules = API_Sub_Engines(
            ai_api_engine=ai_api_engine_modules[engine_modules.ai_api_engine_module](),
            script_db_engine=script_db_engine_modules[
                engine_modules.script_db_engine_module
            ](),
        )

    async def update_session_engines(
        self,
        session: Session,
        engine_modules: Engine_Modules,
    ) -> Union[str, int]:
        if engine_modules.is_empty():
            return -1
        if engine_modules.ai_api_engine_module is not None:
            session.api_engine_modules.ai_api_engine = ai_api_engine_modules[
                engine_modules.ai_api_engine_module
            ]()
        if engine_modules.script_db_engine_module is not None:
            session.api_engine_modules.script_db_engine = script_db_engine_modules[
                engine_modules.script_db_engine_module
            ]()
        return session.session_id

    async def get_session_engine_names(self, session: Session) -> Engine_Modules:
        return Engine_Modules(
            ai_api_engine_module=session.api_engine_modules.ai_api_engine.__class__.__name__,
            script_db_engine_module=session.api_engine_modules.script_db_engine.__class__.__name__,
        )

    # == Session Engine Settings ==
    async def get_session_engine_settings(
        self, session: Session, engine_module_name: str
    ) -> dict:
        return session.api_engine_modules.__getattribute__(
            engine_module_name
        ).get_class_variables()

    async def update_session_engine_settings(
        self,
        session: Session,
        engine_module_name: str,
        engine_settings: dict,
    ) -> Union[str, int]:
        session.api_engine_modules.__getattribute__(
            engine_module_name
        ).set_class_variables(**engine_settings)
        return session.session_id
