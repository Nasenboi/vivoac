'''########################################################################################
Name: audio/models.py
Description: In here are the dictionary models that will be used for the audio routes.
Imports:
'''
from pydantic import BaseModel
from typing import Optional, Union
'''
########################################################################################'''


# audio model
class Audio_Format(BaseModel):
    format: Optional[str]
    codec: Optional[str]
    sample_rate: Optional[int]
    channels: Optional[int]
    bit_rate: Optional[int]
    normalization_type: Optional[str]

    def is_empty(self):
        return not self.__dict__