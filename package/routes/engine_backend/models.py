"""########################################################################################
Name: engine_backend/models.py
Description: 
Imports:
"""

from typing import Dict, Literal, Optional, Type

from pydantic import BaseModel

from ...base_classes import *
from ...modules import *

"""
########################################################################################"""


ai_api_engine_modules: Dict[str, Type[AI_API_Engine]] = {
    # "AI_API_Engine": AI_API_Engine,
    "Piper_TTS_Engine": Piper_TTS_Engine,
}
audio_file_engine_modules: Dict[str, Type[Audio_File_Engine]] = {
    # "Audio_File_Engine": Audio_File_Engine,
    "Basic_Audio_File_Engine": Basic_Audio_File_Engine,
}
script_db_engine_modules: Dict[str, Type[Script_DB_Engine]] = {
    # "Script_DB_Engine": Script_DB_Engine,
    "Excel_Script_DB_Engine": Excel_Script_DB_Engine,
}


class Engine_Modules(BaseModel):
    ai_api_engine_module: Optional[Literal["AI_API_Engine", "Piper_TTS_Engine"]] = None
    audio_file_engine_module: Optional[Literal["Audio_File_Engine"]] = None
    script_db_engine_module: Optional[
        Literal["Script_DB_Engine", "Excel_Script_DB_Engine"]
    ] = None

    def fill_default_values(self):
        self.ai_api_engine_module = self.ai_api_engine_module or "AI_API_Engine"
        self.audio_file_engine_module = (
            self.audio_file_engine_module or "Audio_File_Engine"
        )
        self.script_db_engine_module = (
            self.script_db_engine_module or "Script_DB_Engine"
        )
        return self

    def is_empty(self):
        return not self.__dict__


# api_engine_sub_engines
class API_Sub_Engines(BaseModel):
    session_id: str | int
    ai_api_engine: object = AI_API_Engine()
    audio_file_engine: object = Audio_File_Engine()
    script_db_engine: object = Script_DB_Engine()
