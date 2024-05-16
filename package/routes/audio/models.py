"""########################################################################################
Name: audio/models.py
Description: In here are the dictionary models that will be used for the audio routes.
Imports:
"""

from typing import Optional, Union

from pydantic import BaseModel

"""
########################################################################################"""


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
