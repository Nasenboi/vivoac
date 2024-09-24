"""########################################################################################
Name: engine_backend/models.py
Description: 
Imports:
"""

from typing import Dict, Literal, Optional, Type

from pydantic import BaseModel, field_serializer

from ...base_classes.ai_api_engine import AI_API_Engine
from ...base_classes.script_db_engine import Script_DB_Engine
from ...modules import get_engine_modules

engine_modules = get_engine_modules()

"""
########################################################################################"""

ENGINE_TYPES = Literal["ai_api_engine", "script_db_engine"]

ai_api_engine_modules: Dict[str, Type[AI_API_Engine]] = {
    # "AI_API_Engine": AI_API_Engine,
    "Piper_TTS_Engine": engine_modules["ai_api_engine"]["Piper_TTS_Engine"],
    "ElevenLabs_TTS_Engine": engine_modules["ai_api_engine"]["ElevenLabs_TTS_Engine"],
}
AI_API_ENGINE_MODULE_KEYS = Literal["Piper_TTS_Engine", "ElevenLabs_TTS_Engine"]
script_db_engine_modules: Dict[str, Type[Script_DB_Engine]] = {
    # "Script_DB_Engine": Script_DB_Engine,
    "Excel_Script_DB_Engine": engine_modules["script_db_engine"][
        "Excel_Script_DB_Engine"
    ],
}
SCRIPT_DB_ENGINE_MODULE_KEYS = Literal["Excel_Script_DB_Engine"]


class Engine_Modules(BaseModel):
    ai_api_engine: Optional[Type[AI_API_Engine]] = None
    script_db_engine: Optional[Type[Script_DB_Engine]] = None

    def fill_default_values(self):
        # TODO: maybe its better to throw an error if the engine is not found!
        self.ai_api_engine = ai_api_engine_modules.get("Piper_TTS_Engine")
        self.script_db_engine = script_db_engine_modules.get("Excel_Script_DB_Engine")
        return self

    @field_serializer("ai_api_engine")
    def serialize_ai_api_engine(self, engine: AI_API_Engine, _info):
        return engine.get_class_variables()

    @field_serializer("script_db_engine")
    def serialize_script_db_engine(self, engine: Script_DB_Engine, _info):
        return engine.get_class_variables()

    def is_empty(self):
        return not self.__dict__
