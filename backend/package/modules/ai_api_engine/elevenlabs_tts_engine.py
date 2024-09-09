"""########################################################################################
Name: elevenlabs_tts_engine.py
Description: 

Imports:
"""

import json
import os
from datetime import datetime
from io import BytesIO
from typing import List

import requests
from pydub import AudioSegment

from ...base_classes.ai_api_engine import AI_API_Engine
from ...globals import SETTINGS_GLOBAL
from ...routes.ai_api_handler.models import *
from ...routes.audio.models import *

"""
########################################################################################"""


class ElevenLabs_TTS_Engine(AI_API_Engine):
    # class variables:
    voices: List[Voice_Settings] = []

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        if base_url is None:
            base_url = "https://api.elevenlabs.io/v1"
        super().__init__(api_key=api_key, base_url=base_url, model=model)

        if not self.__url_ok(base_url):
            raise ValueError(f"The given base url: {self.base_url}, is not valid!")

    ############################################################
    # getter functions:

    def get_user_data(self, api_key: str = None) -> dict:
        # No users for this engine!
        return {}

    def get_models(self, api_key: str = None) -> List[str]:
        # No models for this engine!
        return []

    def get_voices(self, api_key: str = None) -> List[str]:
        self.__get_voice_names(api_key)
        voice_names = [voice.name for voice in self.voices]
        return voice_names

    def get_character_voice(self, api_key: str = None, name: str = None) -> str:
        # tbh idk why or what this makes lol
        if name in self.voice_names:
            return name
        return ""

    def get_voice_settings(
        self, api_key: str = None, voice_id: str = None, name: str = None
    ) -> Voice_Settings:
        if name is not None:
            return self.__get_voice_settings_from_name(name)
        elif voice_id is not None:
            return self.__get_voice_settings_from_id(voice_id)

        return Voice_Settings()

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
        path = f"/voices/{voice_settings.voice_id}/settings/edit"
        url = f"{self.base_url}{path}"
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        }

        data = voice_settings.settings

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return

    def delete_voice(
        self, api_key: str = None, voice_id: str = None, name: str = None
    ) -> None:
        voice_id = self.__get_voice_id_from_name(name)
        if len(voice_id) == 0 or voice_id is None:
            return

        path = f"/voices/{voice_id}"
        url = f"{self.base_url}{path}"
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        }

        response = requests.delete(url, headers=headers)
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
        if model is None:
            model = self.model or "eleven_multilangual_v2"

        path = f"/text-to-speech/{voice_settings.voice_id}"
        url = f"{self.base_url}{path}"
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        }

        data = {
            "text": text,
            "voice_settings": voice_settings.settings,
            "seed": seed,
            "model_id": model,
        }

        # type file response

        response = requests.post(url, headers=headers, data=json.dumps(data))
        temp_file_name = "voice" + "_" + datetime.now().strftime("%-y%m%d_%H%M%S")
        temp_file = os.path.join(
            SETTINGS_GLOBAL.get("directories").get("temp"), temp_file_name + ".wav"
        )
        with open(temp_file, "wb") as f:
            for chunk in response.iter_content():
                if chunk:
                    f.write(chunk)
        temp_file: str = self.apply_audio_format(
            target_format=audio_format, audio_file_name=temp_file
        )
        with open(temp_file, "rb") as file:
            data = file.read()
        # lets keep them for now if something bad happens!
        # os.remove(temp_file)
        return data

    ############################################################
    # Private helper functions:

    def __get_voice_names(self, api_key: str = None) -> List[Voice_Settings]:
        path = "/voices"
        url = f"{self.base_url}{path}"
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        voices = data.get("voices", [])
        self.voices.clear()

        for voice in voices:
            v = Voice_Settings()
            v.name = voice.get("name", "No name available!")
            v.voice_id = voice.get("voice_id", "No id available!")
            v.description = voice.get("description", "No description available!")
            v.labels = voice.get("labels", {"Messages": "No labels available!"})
            v.files = [file["file_name"] for file in voice.get("files", [])]
            v.settings = voice.get("voice_settings", {})
            self.voices.append(v)

        return v

    def __get_voice_id_from_name(self, name: str = None) -> str:
        for voice in self.voices:
            if voice.name == name:
                return voice.voice_id

    def __get_voice_settings_from_name(self, name: str = None) -> Voice_Settings:
        for voice in self.voices:
            if voice.name == name:
                return voice
        return Voice_Settings()

    def __get_voice_settings_from_id(
        self, voice_id: Union[int, str] = None
    ) -> Voice_Settings:
        for voice in self.voices:
            if voice.voice_id == voice_id:
                return voice
        return Voice_Settings()

    @staticmethod
    def __url_ok(url):
        return True  # trust the process!
        r = requests.head(url)
        return r.status_code == 200
