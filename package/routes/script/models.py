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
    id: Optional[Union[int, str]]
    character_name: Optional[str]
    voice_talent: Optional[str]
    script_name: Optional[str]
    number_of_lines: Optional[int]
    gender: Optional[str]


# script model
class Script(BaseModel):
    id: Optional[Union[int, str]]
    source_text: Optional[str]
    translation: Optional[str]
    time_restriction: Optional[Union[str, int]]
    voice_talent: Optional[str]
    character_name: Optional[str]
    reference_audio_path: Optional[str]
    delivery_audio_path: Optional[str]
    generatied_audio_path: Optional[str]

    def is_empty(self):
        return not self.__dict__
