'''########################################################################################
Name: script/functions.py
Description: 
Imports:
'''
from .models import *
from typing import Union, List
from ...globals import LOGGER, SETTINGS_GLOBAL
from fastapi import HTTPException
'''
########################################################################################'''


def get_script(script: Script) -> Union[List[Union[Script]], Script]:
    LOGGER.debug(f"Getting script: {script}")
    
    if script.is_empty():
        LOGGER.warning(f"Recieved an empty script")
        raise HTTPException(status_code=400, detail="Recieved an empty script")
    
