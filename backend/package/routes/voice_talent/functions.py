"""########################################################################################
Name: voice_talent/functions.py
Description: 
Imports:
"""

from fastapi import HTTPException
from ...globals import LOGGER

from bson import ObjectId

from typing import List

from .models import *
from ...db import DB_COLLECTIONS

"""
########################################################################################"""


async def get_voice_talent(voice_talent_id: PydanticObjectId = None) -> Voice_Talent:
    try:
        voice_talent = DB_COLLECTIONS["voice_talents"].find_one(
            {"_id": voice_talent_id}
        )

        if not voice_talent:
            raise Exception("Voice Talent not found")

        voice_talent = Voice_Talent.model_validate(voice_talent)
    except Exception as e:
        LOGGER.error(f"Error getting voice talent: {e}")
        raise HTTPException(status_code=404, detail="Voice Talent not found")
    return voice_talent


async def find_voice_talents(voice_talent_query: dict = {}) -> List[Voice_Talent]:
    try:
        query = {k: v for k, v in voice_talent_query.items() if v is not None and k not in ["_id", "created_at", "updated_at"]}
        voice_talents = list(DB_COLLECTIONS["voice_talents"].find(query))
    except Exception as e:
        LOGGER.error(f"Error finding voice talents: {e}")
        raise HTTPException(status_code=404, detail="Voice Talents not found")
    return [Voice_Talent.model_validate(voice_talent) for voice_talent in voice_talents]


async def create_voice_talent(voice_talent: Voice_Talent) -> Voice_Talent:
    try:
        # check if there are any voice talents with the same name:
        voice_talents = await find_voice_talents(
            voice_talent_query={
                "first_name": voice_talent.first_name,
                "last_name": voice_talent.last_name,
            }
        )
        if len(voice_talents) > 0:
            raise HTTPException(
                status_code=400,
                detail="A voice talent this name does with already exists",
            )

        # insert voice talent
        voice_talent_id = (
            DB_COLLECTIONS["voice_talents"]
            .insert_one(voice_talent.model_dump())
            .inserted_id
        )
        voice_talent = await get_voice_talent(voice_talent_id)
    except Exception as e:
        LOGGER.error(f"Error creating voice talent: {e}")
        raise HTTPException(status_code=500, detail="Error creating voice talent")
    return voice_talent


async def update_voice_talent(
    voice_talent_id: str, voice_talent: Voice_Talent
) -> Voice_Talent:
    try:
        voice_talent_update = {
            k: v
            for k, v in voice_talent.model_dump().items()
            if v and k not in ["_id", "created_at"]
        }

        # update voice talent
        DB_COLLECTIONS["voice_talents"].update_one(
            {"_id": voice_talent_id}, {"$set": voice_talent_update}
        )
        voice_talent = await get_voice_talent(voice_talent_id=voice_talent_id)
    except Exception as e:
        LOGGER.error(f"Error updating voice talent: {e}")
        raise HTTPException(status_code=500, detail="Error updating voice talent")
    return voice_talent


async def delete_voice_talent(voice_talent_id: PydanticObjectId) -> Voice_Talent:
    try:
        # check if voice talent exists and fetch it
        voice_talent = await get_voice_talent(voice_talent_id=voice_talent_id)
        # delete voice talent
        DB_COLLECTIONS["voice_talents"].delete_one({"_id": voice_talent_id})
    except Exception as e:
        LOGGER.error(f"Error deleting voice talent: {e}")
        raise HTTPException(status_code=500, detail="Error deleting voice talent")
    return voice_talent
