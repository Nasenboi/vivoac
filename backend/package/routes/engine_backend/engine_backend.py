"""########################################################################################
Name: engine_backend/engine_backend.py
Description: 
Imports:
"""

from typing import Any, Dict, Union

from fastapi import HTTPException

from ...modules import get_engine_modules
from .models import *

engine_modules = get_engine_modules()

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
            ai_api_engine_module, engine_modules["ai_api_engine"]["Piper_TTS_Engine"]
        )()
        self.engine_modules.script_db_engine = script_db_engine_modules.get(
            script_db_engine_module,
            engine_modules["script_db_engine"]["Excel_Script_DB_Engine"],
        )()

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
        engine_type: ENGINE_TYPES,
        module: Union[AI_API_ENGINE_MODULE_KEYS, SCRIPT_DB_ENGINE_MODULE_KEYS],
    ) -> Dict[str, str]:
        if (
            engine_type == "ai_api_engine"
            and module != self.engine_modules.ai_api_engine.__class__.__name__
            and ai_api_engine_modules.get(module)
        ):
            self.engine_modules.ai_api_engine = ai_api_engine_modules.get(module)()
        elif (
            engine_type == "script_db_engine"
            and module != self.engine_modules.script_db_engine.__class__.__name__
            and script_db_engine_modules.get(module)
        ):
            self.engine_modules.script_db_engine = script_db_engine_modules.get(
                module
            )()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid engine type or module: {engine_type}, {module}",
            )
        return {
            engine_type: module,
        }

    async def update_engine_module_settings(
        self,
        engine_type: ENGINE_TYPES,
        settings: dict = None,
    ) -> Dict[str, Any]:
        if engine_type == "ai_api_engine":
            self.engine_modules.ai_api_engine.set_class_variables(settings)
            return {
                engine_type: await self.get_ai_api_engine_settings(),
            }
        elif engine_type == "script_db_engine":
            self.engine_modules.script_db_engine.set_class_variables(settings)
            return {
                engine_type: await self.get_script_db_engine_settings(),
            }
