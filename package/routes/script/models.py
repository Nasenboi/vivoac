'''########################################################################################
Name: script/models.py
Description: In here are the dictionary models that will be used for the script routes.
Imports:
'''
from pydantic import BaseModel
from typing import Optional, Union
'''
########################################################################################'''

# script model
class Script(BaseModel):
    id: Optional[Union[int, str]]
    source_text: Optional[str]
    translation: Optional[str]
    time_restriction: Optional[Union[str, int]]
    voice_talent: Optional[str]
    character: Optional[str]
    reference_audio_path: Optional[str]
    delivery_audio_path: Optional[str]
    generatied_audio_path: Optional[str]

    def is_empty(self):
        return not self.__dict__