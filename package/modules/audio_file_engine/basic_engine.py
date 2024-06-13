"""########################################################################################
Name: modules/audio_file_engine/basic.py
Description: 
Imports:
"""

from typing import List, Union

from ...base_classes import Audio_File_Engine
from ...routes.audio.models import Audio_Format

"""
########################################################################################"""


class Basic_Audio_File_Engine(Audio_File_Engine):

    def __init__(self, target_format: Audio_Format = None):
        self.target_format = target_format

    ############################################################
    # getter functions:

    def get_audio_files(
        self, file_paths=Union[List[str], str]
    ) -> Union[List[bytes], bytes]:
        pass

    ############################################################
    # Audio file functions:

    def save_audio_file(self, file_path: str, audio_data: bytes) -> None:
        pass

    def delete_audio_file(self, file_path: str) -> None:
        pass

    def standardize_audio_file(self, file_path: str) -> bytes:
        pass
