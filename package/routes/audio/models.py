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
    codec: Optional[Literal["wav", "mp3", "ogg", "aiff"]] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    bit_depth: Optional[int] = None
    bit_rate: Optional[int] = None
    normalization_type: Optional[Literal["None", "Peak", "Loudness"]] = None

    def fill_default_values(self):
        self.codec = self.codec or "wav"
        self.sample_rate = self.sample_rate or 192_000
        self.channels = self.channels or 2
        self.bit_depth = self.bit_depth or 16
        self.bit_rate = self.bit_rate or 320_000
        self.normalization_type = self.normalization_type or "None"
        return self

    def is_empty(self):
        return not self.__dict__
