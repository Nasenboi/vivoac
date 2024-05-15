'''########################################################################################
Name: script_db_engine.py
Description: 
Imports:
'''
from ..routes.script.models import Script
from ..utils.decorators import virtual
from typing import List, Union
'''
########################################################################################'''

class Script_DB_Engine():
    # class variables:

    def __init__(self):
        pass


    ############################################################
    # getter functions:

    @virtual
    def get_script_lines(self, script: Script = Script()) -> Union[List[Script], Script]:
        pass