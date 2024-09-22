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

from ...base_classes.ai_api_engine import AI_API_Engine
from ...globals import LOGGER, SETTINGS_GLOBAL
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
    piper_voice_directory = SETTINGS_GLOBAL.get("directories").get("piper_voices", "")
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
        self.__get_voice_names()
        return self.voice_names

    def get_character_voice(self, api_key: str = None, name: str = None) -> str:
        if name in self.voice_names:
            return name
        return ""

    def get_voice_settings(
        self, api_key: str = None, voice_id: str = None, name: str = None
    ) -> Voice_Settings:
        if voice_id is None:
            voice_id = name
        settings_path = os.path.join(
            self.piper_voice_directory, f"{voice_id}.onnx.json"
        )
        settings = {}
        try:
            if os.path.isfile(settings_path):
                with open(settings_path, "r") as file:
                    settings = json.load(file)
        except Exception as e:
            LOGGER.error(f"Error getting voice settings: {e}")
            settings = {}

        voice_settings = Voice_Settings(
            voice_id=voice_id,
            name=voice_id,
            settings=settings,
            description="No description available!",
            files=["No files available!"],
            labels={"Messages": "No labels available!"},
        )
        LOGGER.debug(f"Voice settings: {voice_settings}")
        return voice_settings

    ############################################################
    # Voice editing functions:

    def create_voice(
        self,
        api_key: str = None,
        voice_settings: Voice_Settings = None,
    ) -> str:
        raise NotImplementedError

    def edit_voice_settings(
        self,
        api_key: str = None,
        voice_settings: Voice_Settings = None,
    ) -> None:
        settings_path = os.path.join(
            self.piper_voice_directory, f"{voice_settings.voice_id}.onnx.json"
        )
        if os.path.isfile(settings_path):
            with open(settings_path, "w") as file:
                json.dump(voice_settings.settings, file)

        return

    def delete_voice(
        self, api_key: str = None, voice_id: str = None, name: str = None
    ) -> None:
        if voice_id is None:
            voice_id = name
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

        temp_file_name = "voice" + "_" + datetime.now().strftime("%-y%m%d_%H%M%S")
        temp_file = os.path.join(
            SETTINGS_GLOBAL.get("directories").get("temp"), temp_file_name + ".wav"
        )
        dt = Dimits(voice=voice, modelDirectory=self.piper_voice_directory)
        dt.text_2_audio_file(
            text,
            temp_file_name.split(".wav")[0],
            temp_file.split(temp_file_name)[0],
            format="wav",
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
        self.voice_names = []
        if self.piper_voice_directory == "" or not os.path.isdir(
            self.piper_voice_directory
        ):
            return

        for file in os.listdir(self.piper_voice_directory):
            if file.endswith(".onnx"):
                self.voice_names.append(file.split(".")[0])

        # get all files inside of the voice directory
        ending = ".onnx"
        self.voice_names = [
            file.split(".")[0]
            for file in os.listdir(self.piper_voice_directory)
            if file.endswith(ending)
        ]
        return
