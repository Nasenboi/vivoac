"""########################################################################################
Name: voice/functions.py
Description: 
Imports:
"""

from typing import List

from fastapi import HTTPException

from ...db import DB_COLLECTIONS
from ...globals import LOGGER
from ...utils.models import PydanticObjectId
from .models import Voice

"""
########################################################################################"""


async def get_voice(voice_id: PydanticObjectId = None) -> Voice:
    try:
        voice = DB_COLLECTIONS["voices"].find_one({"_id": voice_id})

        if not voice:
            raise Exception("Voice not found")

        voice = Voice.model_validate(voice)
    except Exception as e:
        LOGGER.error(f"Error getting voice: {e}")
        raise HTTPException(status_code=404, detail="Voice not found")
    return voice


async def find_voices(voice_query: dict = {}) -> List[Voice]:
    try:
        query = {
            k: v
            for k, v in voice_query.items()
            if v is not None and k not in ["_id", "created_at", "updated_at"]
        }
        voices = list(DB_COLLECTIONS["voices"].find(query))
    except Exception as e:
        LOGGER.error(f"Error finding voices: {e}")
        raise HTTPException(status_code=404, detail="Voices not found")
    return [Voice.model_validate(voice) for voice in voices]


async def create_voice(voice: Voice) -> Voice:
    try:
        # check if there are any voices with the same name:
        voices = await find_voices(
            voice_query={
                "first_name": voice.first_name,
                "last_name": voice.last_name,
            }
        )
        if len(voices) > 0:
            raise HTTPException(
                status_code=400,
                detail="A voice this name does with already exists",
            )

        # insert voice
        voice_id = DB_COLLECTIONS["voices"].insert_one(voice.model_dump()).inserted_id
        voice = await get_voice(voice_id)
    except Exception as e:
        LOGGER.error(f"Error creating voice: {e}")
        raise HTTPException(status_code=500, detail="Error creating voice")
    return voice


async def update_voice(voice_id: str, voice: Voice) -> Voice:
    try:
        voice_update = {
            k: v
            for k, v in voice.model_dump().items()
            if v and k not in ["_id", "created_at"]
        }

        # update voice
        DB_COLLECTIONS["voices"].update_one({"_id": voice_id}, {"$set": voice_update})
        voice = await get_voice(voice_id=voice_id)
    except Exception as e:
        LOGGER.error(f"Error updating voice: {e}")
        raise HTTPException(status_code=500, detail="Error updating voice")
    return voice


async def delete_voice(voice_id: PydanticObjectId) -> Voice:
    try:
        # check if voice exists and fetch it
        voice = await get_voice(voice_id=voice_id)
        # delete voice
        DB_COLLECTIONS["voices"].delete_one({"_id": voice_id})
    except Exception as e:
        LOGGER.error(f"Error deleting voice: {e}")
        raise HTTPException(status_code=500, detail="Error deleting voice")
    return voice
