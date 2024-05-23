"""########################################################################################
Name: engine_backend/models.py
Description: 
Imports:
"""

from typing import Literal, Type, Union

from pydantic import BaseModel

from ...base_classes import *

"""
########################################################################################"""


# api_engine_sub_engines
class API_Sub_Engines(BaseModel):
    session_id: str | int
    ai_api_engine: Type[AI_API_Engine] = AI_API_Engine()
    audio_file_engine: Type[Audio_File_Engine] = Audio_File_Engine()
    script_db_engine: Type[Script_DB_Engine] = Script_DB_Engine()
