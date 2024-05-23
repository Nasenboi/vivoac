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

    def add_session_engines(
        self,
        session_id: str | int,
        engine_modules: Optional[Engine_Modules] = Engine_Modules(),
    ):
        LOGGER.debug(
            f"{ai_api_engine_modules[engine_modules.ai_api_engine_module]().__class__}"
        )
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
        LOGGER.debug("2")

    def change_session_engines(
        self,
        session_id: str | int,
        engine_modules: Engine_Modules,
    ) -> str | int:
        if engine_modules.is_empty():
            return
        for session in self.session_sub_engines:
            if session.session_id == session_id:
                if engine_modules.ai_api_engine_module is not None:
                    session.ai_api_engine = ai_api_engine_modules[
                        engine_modules.ai_api_engine_module
                    ]()
                if engine_modules.audio_file_engine_module is not None:
                    session.audio_file_engine = audio_file_engine_modules[
                        engine_modules.audio_file_engine_module
                    ]()
                if engine_modules.script_db_engine_module is not None:
                    session.script_db_engine = script_db_engine_modules[
                        engine_modules.script_db_engine_module
                    ]()
                return session_id

    def get_session_engines(self, session_id: str | int) -> API_Sub_Engines:
        for session in self.session_sub_engines:
            if session.session_id == session_id:
                return session

    def close_session_engines(self, session_id: str | int) -> str | int:
        for session in self.session_sub_engines:
            if session.session_id == session_id:
                self.session_sub_engines.remove(session)
                return session_id
