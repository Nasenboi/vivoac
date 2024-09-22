"""########################################################################################
Name: api_engine/api_engine_base.py
Description: The api engine base class is used for better intellisece and code completion
Imports:
"""

from ..base_classes.ai_api_engine import AI_API_Engine
from ..base_classes.script_db_engine import Script_DB_Engine
from ..routes.engine_backend.engine_backend import Engine_Backend

# from threading import Thread
"""
########################################################################################"""


class API_Engine_Base:
    # define class variables
    engine_backend: Engine_Backend = None

    # quick access to the module engines
    @property
    def ai_api_engine(self) -> AI_API_Engine:
        return self.engine_backend.engine_modules.ai_api_engine

    @property
    def script_db_engine(self) -> Script_DB_Engine:
        return self.engine_backend.engine_modules.script_db_engine
