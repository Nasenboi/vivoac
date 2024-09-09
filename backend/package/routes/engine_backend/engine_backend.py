"""########################################################################################
Name: engine_backend/engine_backend.py
Description: 
Imports:
"""

from typing import Dict, Any

from .models import *

from ...modules import *

"""
########################################################################################"""


class Engine_Backend:
    engine_modules: Engine_Modules = Engine_Modules()

    def __init__(
        self,
        ai_api_engine_module: AI_API_ENGINE_MODULE_KEYS = "Piper_TTS_Engine",
        script_db_engine_module: SCRIPT_DB_ENGINE_MODULE_KEYS = "Excel_Script_DB_Engine",
    ):
        self.engine_modules.ai_api_engine = ai_api_engine_modules.get(
            ai_api_engine_module, Piper_TTS_Engine
        )
        self.engine_modules.script_db_engine = script_db_engine_modules.get(
            script_db_engine_module, Excel_Script_DB_Engine
        )

    async def get_ai_api_engine_name(self) -> str:
        return self.engine_modules.ai_api_engine.__class__.__name__

    async def get_script_db_engine_name(self) -> str:
        return self.engine_modules.script_db_engine.__class__.__name__

    async def get_ai_api_engine_settings(self) -> dict:
        return self.engine_modules.ai_api_engine.get_class_variables()

    async def get_script_db_engine_settings(self) -> dict:
        return self.engine_modules.script_db_engine.get_class_variables()

    async def set_engine_module(
        self,
        ai_api_engine_module: AI_API_ENGINE_MODULE_KEYS = None,
        script_db_engine_module: SCRIPT_DB_ENGINE_MODULE_KEYS = None,
    ) -> Dict[str, str]:
        self.engine_modules.ai_api_engine = (
            ai_api_engine_modules.get(ai_api_engine_module, Piper_TTS_Engine)
            if ai_api_engine_module
            else self.engine_modules.ai_api_engine
        )
        self.engine_modules.script_db_engine = (
            script_db_engine_modules.get(
                script_db_engine_module, Excel_Script_DB_Engine
            )
            if script_db_engine_module
            else self.engine_modules.script_db_engine
        )
        return {
            "ai_api_engine": await self.get_ai_api_engine_name(),
            "script_db_engine": await self.get_script_db_engine_name(),
        }

    async def update_engine_module_settings(
        self,
        ai_api_engine_settings: dict = None,
        script_db_engine_settings: dict = None,
    ) -> Dict[str, Dict[str, Any]]:
        if ai_api_engine_settings:
            self.engine_modules.ai_api_engine.set_class_variables(
                ai_api_engine_settings
            )
        if script_db_engine_settings:
            self.engine_modules.script_db_engine.set_class_variables(
                script_db_engine_settings
            )
        return {
            "ai_api_engine": await self.get_ai_api_engine_settings(),
            "script_db_engine": await self.get_script_db_engine_settings(),
        }
