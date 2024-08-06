"""########################################################################################
Name: engine_backend/models.py
Description: 
Imports:
"""

from typing import Dict, Literal, Optional, Type

from pydantic import BaseModel, field_serializer

from ...base_classes import *
from ...modules import *

"""
########################################################################################"""


ai_api_engine_modules: Dict[str, Type[AI_API_Engine]] = {
    # "AI_API_Engine": AI_API_Engine,
    "Piper_TTS_Engine": Piper_TTS_Engine,
    "ElevenLabs_TTS_Engine": ElevenLabs_TTS_Engine,
}
script_db_engine_modules: Dict[str, Type[Script_DB_Engine]] = {
    # "Script_DB_Engine": Script_DB_Engine,
    "Excel_Script_DB_Engine": Excel_Script_DB_Engine,
}


class Engine_Modules(BaseModel):
    ai_api_engine_module: Optional[
        Literal["Piper_TTS_Engine", "ElevenLabs_TTS_Engine"]
    ] = None
    script_db_engine_module: Optional[Literal["Excel_Script_DB_Engine"]] = None

    def fill_default_values(self):
        self.ai_api_engine_module = self.ai_api_engine_module or "Piper_TTS_Engine"
        self.script_db_engine_module = (
            self.script_db_engine_module or "Excel_Script_DB_Engine"
        )
        return self

    def is_empty(self):
        return not self.__dict__


# api_engine_sub_engines
class API_Sub_Engines(BaseModel):
    ai_api_engine: Optional[Type[AI_API_Engine]] = None
    script_db_engine: Optional[Type[Script_DB_Engine]] = None

    @field_serializer("ai_api_engine")
    def serialize_ai_api_engine(self, engine: AI_API_Engine, _info):
        return engine.get_class_variables()

    @field_serializer("script_db_engine")
    def serialize_script_db_engine(self, engine: Script_DB_Engine, _info):
        return engine.get_class_variables()
