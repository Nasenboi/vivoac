"""########################################################################################
Name: api_engine/models.py
Description: alround models that can be used across the whole project
Imports:
"""

from typing import Literal, Optional

from pydantic import BaseModel

"""
########################################################################################"""


# audio model
class Audio_Format(BaseModel):
    codec: Optional[Literal["aac", "mp3", "ogg", "wav"]] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    bit_depth: Optional[int] = None
    bit_rate: Optional[int] = None
    normalization_type: Optional[Literal["None", "Peak", "Loudness"]] = None

    def map_mime_type(self) -> str:
        map_dict = {
            "aac": "audio/aac",
            "mp3": "audio/mpeg",
            "ogg": "audio/ogg",
            "wav": "audio/wav",
        }
        return map_dict.get(self.codec, None)

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
