'''########################################################################################
Name: audio_file_engine.py
Description: 
Imports:
'''
from ..utils.decorators import virtual
from typing import List, Union
from ..routes.audio.models import Audio_Format
'''
########################################################################################'''


class Audio_File_Engine():
    # class variables:
    target_format: Audio_Format = None

    def __init__(self, target_format: Audio_Format = None):
        self.target_format = target_format


    ############################################################
    # getter functions:


    @virtual
    def get_audio_files(self, file_paths = Union[List[str], str]) -> Union[List[bytes], bytes]:
        pass

    ############################################################
    # Audio file functions:

    @virtual
    def save_audio_file(self, file_path: str, audio_data: bytes) -> None:
        pass


    @virtual
    def delete_audio_file(self, file_path: str) -> None:
        pass

    @virtual
    def standardize_audio_file(self, file_path: str) -> bytes:
        pass