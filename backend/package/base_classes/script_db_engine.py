"""########################################################################################
Name: base_classes/script_db_engine.py
Description: 
Imports:
"""

from typing import List, Optional, Union

from ..routes.script.models import Character_Info, Script_Line
from ..utils.decorators import virtual
from .base_engine import Base_Engine

"""
########################################################################################"""


class Script_DB_Engine(Base_Engine):
    # class variables:
    script_name: str = None

    def __init__(self, script_name: str = None):
        self.script_name = script_name

    ############################################################
    # getter functions:

    @virtual
    def get_script_names(self) -> List[str]:
        pass

    @virtual
    def get_script_lines(
        self, script: Optional[Script_Line] = Script_Line()
    ) -> List[Script_Line]:
        pass

    @virtual
    def get_character_infos(
        self, character_info: Character_Info = Character_Info()
    ) -> Union[List[Character_Info], Character_Info]:
        pass
