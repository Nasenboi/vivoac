"""########################################################################################
Name: ai_api_engine/piper_tts_engine.py
Description: The base class for all AI API Engine classes
Most of the functions are build after the ElevenLabs API but can be adapted to other APIs,
because thats what the modular child classes are for!
Imports:
"""

import json
import os
import sys
from datetime import datetime
from typing import List

# only import if device is running on linux
if sys.platform == "linux":
    from dimits import Dimits

from ...base_classes import AI_API_Engine
from ...globals import SETTINGS_GLOBAL
from ...routes.ai_api_handler.models import *
from ...routes.audio.models import *

"""
Notes:
Use dimits to call piper api functions!
from dimits import dimits
model_name = de_DE_Name_pitch(.onnx)
dt = Dimits(voice="model_name", modelDirectory="model_directory")
dt.text_2_audio_file("text", "file_name", "output_directory", format="wav")

########################################################################################"""


class Piper_TTS_Engine(AI_API_Engine):
    # class variables:
    piper_voice_directory = SETTINGS_GLOBAL.get("directories").get("piper-voice", "")
    voice_names: List[str] = []

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        super().__init__(api_key=api_key, base_url=base_url, model=model)

        self.__get_voice_names()

    ############################################################
    # getter functions:

    def get_user_data(self, api_key: str = None) -> dict:
        # No users for this engine!
        return {}

    def get_models(self, api_key: str = None) -> List[str]:
        # No models for this engine!
        return []

    def get_voices(self, api_key: str = None) -> List[str]:
        return self.voice_names

    def get_character_voice(self, api_key: str = None, name: str = None) -> str:
        if name in self.voice_names:
            return name
        return ""

    def get_voice_settings(self, api_key: str = None, voice_id: str = None) -> dict:
        settings_path = os.path.join(
            self.piper_voice_directory, f"{voice_id}.onnx.json"
        )
        if os.path.isfile(settings_path):
            with open(settings_path, "r") as file:
                return json.load(file)
        return {}

    ############################################################
    # Voice editing functions:

    def create_voice(
        self,
        api_key: str = None,
        name: str = None,
        description: str = None,
        files: List[str] = None,
        labels: dict = None,
    ) -> str:
        raise NotImplementedError

    def edit_voice_settings(
        self,
        api_key: str = None,
        voice_id: str = None,
        name: str = None,
        description: str = None,
        files: List[str] = None,
        labels: dict = None,
        settings: dict = None,
    ) -> None:
        settings_path = os.path.join(
            self.piper_voice_directory, f"{voice_id}.onnx.json"
        )
        if os.path.isfile(settings_path):
            with open(settings_path, "w") as file:
                json.dump(settings, file)

        return

    def delete_voice(self, api_key: str = None, voice_id: str = None) -> None:
        # This may be a bit dangerous, but we will allow it for now!
        voice_path = os.path.join(self.piper_voice_directory, f"{voice_id}.onnx")
        settings_path = os.path.join(
            self.piper_voice_directory, f"{voice_id}.onnx.json"
        )
        if os.path.isfile(voice_path):
            os.remove(voice_path)

        if os.path.isfile(settings_path):
            os.remove(settings_path)

        return

    ############################################################
    # Text to Speech

    def text_to_speech(
        self,
        api_key: str = None,
        text: str = None,
        voice: str = None,
        voice_settings: Voice_Settings = None,
        model: str = None,
        seed: int = None,
        audio_format: Audio_Format = None,
    ) -> bytes:
        if sys.platform != "linux":
            raise OSError("This function is only available on linux devices!")

        temp_file = os.path.join(
            SETTINGS_GLOBAL.get("directories").get("temp"),
            "voice" + "_" + datetime.now().strftime("%-y%m%d_%H%M%S") + ".wav",
        )
        dt = Dimits(voice=voice, modelDirectory=self.piper_voice_directory)
        dt.text_2_audio_file(
            text, temp_file.split(".wav")[0], self.piper_voice_directory, format="wav"
        )
        temp_file: str = self.apply_audio_format(
            target_format=audio_format, audio_file_name=temp_file
        )
        with open(temp_file, "rb") as file:
            data = file.read()
        os.remove(temp_file)
        return data

    ############################################################
    # Private Functions:

    def __get_voice_names(self) -> None:
        if (
            self.piper_voice_directory == ""
            or os.path.isdir(self.piper_voice_directory) == False
        ):
            self.voice_names = []
            return

        # get all files inside of the voice directory
        ending = ".onnx"
        self.voice_names = [
            file.split(".")[0]
            for file in os.listdir(self.piper_voice_directory)
            if file.endswith(ending)
        ]
        return
