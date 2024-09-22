"""########################################################################################
Name: api_engine/api_engine.py
Description: The api engine is the core class of this project.
This engine will manage all the sub - components and is responsible for the main loop
Imports:
"""

from typing import List

from fastapi import APIRouter

from ..base_classes.ai_api_engine import AI_API_Engine
from ..base_classes.script_db_engine import Script_DB_Engine
from ..globals import *
from .class_functions import *

# from threading import Thread
"""
########################################################################################"""


class API_Engine:
    # define class variables
    app = None
    routes: List[APIRouter] = []
    config = None
    uvicorn_server = None
    uvicorn_thread = None
    engine_backend = None

    def __init__(self, *args, **kwargs):
        init(self, *args, **kwargs)

    def run(self, *args, **kwargs):
        run(self, *args, **kwargs)

    def stop(self, *args, **kwargs):
        stop(self, *args, **kwargs)

    # quick access to the module engines
    @property
    def ai_api_engine(self) -> AI_API_Engine:
        return self.engine_backend.engine_modules.ai_api_engine

    @property
    def script_db_engine(self) -> Script_DB_Engine:
        return self.engine_backend.engine_modules.script_db_engine
