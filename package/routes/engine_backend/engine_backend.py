"""########################################################################################
Name: engine_backend/engine_backend.py
Description: 
Imports:
"""

from typing import List, Optional

from ...globals import LOGGER
from .models import *

"""
########################################################################################"""


class Engine_Backend:
    session_sub_engines: List[API_Sub_Engines] = []

    async def add_session_engines(
        self,
        session_id: str | int,
        engine_modules: Optional[
            Engine_Modules
        ] = Engine_Modules().fill_default_values(),
    ):
        LOGGER.debug(f"Adding session engines: {session_id}")
        self.session_sub_engines.append(
            API_Sub_Engines(
                session_id=session_id,
                ai_api_engine=ai_api_engine_modules[
                    engine_modules.ai_api_engine_module
                ](),
                audio_file_engine_modules=audio_file_engine_modules[
                    engine_modules.audio_file_engine_module
                ](),
                script_db_engine_modules=script_db_engine_modules[
                    engine_modules.script_db_engine_module
                ](),
            )
        )

    async def update_session_engines(
        self,
        session_id: str | int,
        engine_modules: Engine_Modules,
    ) -> str | int:
        if engine_modules.is_empty():
            return
        for engine in self.session_sub_engines:
            if engine.session_id == session_id:
                if engine_modules.ai_api_engine_module is not None:
                    engine.ai_api_engine = ai_api_engine_modules[
                        engine_modules.ai_api_engine_module
                    ]()
                if engine_modules.audio_file_engine_module is not None:
                    engine.audio_file_engine = audio_file_engine_modules[
                        engine_modules.audio_file_engine_module
                    ]()
                if engine_modules.script_db_engine_module is not None:
                    engine.script_db_engine = script_db_engine_modules[
                        engine_modules.script_db_engine_module
                    ]()
                return session_id
        raise ValueError(f"Session ID not found: {session_id}")

    async def get_session_engines(self, session_id: str | int) -> API_Sub_Engines:
        for engine in self.session_sub_engines:
            if engine.session_id == session_id:
                return engine
        raise ValueError(f"Session ID not found: {session_id}")

    async def get_session_engine_names(self, session_id: str | int) -> Engine_Modules:
        for engine in self.session_sub_engines:
            if engine.session_id == session_id:
                return Engine_Modules(
                    ai_api_engine_module=engine.ai_api_engine.__class__.__name__,
                    audio_file_engine_module=engine.audio_file_engine.__class__.__name__,
                    script_db_engine_module=engine.script_db_engine.__class__.__name__,
                )
        raise ValueError(f"Session ID not found: {session_id}")

    async def close_session_engines(self, session_id: str | int) -> str | int:
        for engine in self.session_sub_engines:
            if engine.session_id == session_id:
                self.session_sub_engines.remove(engine)
                return session_id
        raise ValueError(f"Session ID not found: {session_id}")

    # == Session Engine Settings ==
    async def get_session_engine_settings(
        self, session_id: str | int, engine_module_name: str
    ) -> dict:
        for engine in self.session_sub_engines:
            if engine.session_id == session_id:
                return engine.__getattribute__(engine_module_name).get_class_variables()
        raise ValueError(f"Session ID not found: {session_id}")

    async def update_session_engine_settings(
        self, session_id: str | int, engine_module_name: str, engine_settings: dict
    ) -> str | int:
        for engine in self.session_sub_engines:
            if engine.session_id == session_id:
                engine.__getattribute__(engine_module_name).set_class_variables(
                    **engine_settings
                )
                return session_id
        raise ValueError(f"Session ID not found: {session_id}")
