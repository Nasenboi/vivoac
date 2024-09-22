"""########################################################################################
Name: script/functions.py
Description: 
Imports:
"""

from typing import List

from ...base_classes.script_db_engine import Script_DB_Engine
from ...globals import LOGGER
from .models import *

"""
########################################################################################"""


async def get_script_lines(
    script_line: Optional[Script_Line], script_db_engine: Script_DB_Engine
) -> List[Script_Line]:
    LOGGER.debug(f"Getting script: {script_line}")
    return script_db_engine.get_script_lines(script_line)
