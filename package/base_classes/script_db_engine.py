'''########################################################################################
Name: script_db_engine.py
Description: 
Imports:
'''
from ..routes.script.models import Script, Character_Info
from ..utils.decorators import virtual
from typing import List, Union
'''
########################################################################################'''

class Script_DB_Engine():
    # class variables:
    script_name: str = None

    def __init__(self, script_name: str = None):
        pass

    ############################################################
    # getter functions:

    @virtual
    def get_script_names(self) -> List[str]:
        pass

    @virtual
    def get_script_lines(self, script: Script = Script()) -> Union[List[Script], Script]:
        pass

    @virtual
    def get_character_infos(self, character_info: Character_Info = Character_Info()) -> Union[List[Character_Info], Character_Info]:
        pass