"""########################################################################################
Name: audio/models.py
Description: In here are the dictionary models that will be used for the audio routes.
Imports:
"""

from typing import Literal, Optional

from pydantic import BaseModel

"""
########################################################################################"""


# audio model
class Audio_Format(BaseModel):
    codec: Optional[Literal["wav", "mp3", "ogg", "aiff"]] = "wav"
    sample_rate: Optional[int] = 192_000
    channels: Optional[int] = 2
    bit_depth: Optional[int] = 16
    bit_rate: Optional[int] = 320_000
    normalization_type: Optional[Literal["None", "Peak", "Loudness"]] = "None"

    def is_empty(self):
        return not self.__dict__
