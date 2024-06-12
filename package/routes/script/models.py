"""########################################################################################
Name: script/models.py
Description: In here are the dictionary models that will be used for the script routes.
Imports:
"""

from typing import Optional, Union

from pydantic import BaseModel

"""
########################################################################################"""


# character into model
class Character_Info(BaseModel):
    id: Optional[Union[int, str]] = None
    character_name: Optional[str] = None
    voice_talent: Optional[str] = None
    script_name: Optional[str] = None
    number_of_lines: Optional[int] = None
    gender: Optional[str] = None

    def is_empty(self):
        return not self.__dict__


# script model
class Script_Line(BaseModel):
    id: Optional[Union[int, str]] = None
    source_text: Optional[str] = None
    translation: Optional[str] = None
    time_restriction: Optional[Union[str, int]] = None
    voice_talent: Optional[str] = None
    character_name: Optional[str] = None
    reference_audio_path: Optional[str] = None
    delivery_audio_path: Optional[str] = None
    generated_audio_path: Optional[str] = None
    comment: Optional[str] = None
    direction_notes: Optional[str] = None

    def is_empty(self):
        return not self.__dict__
