"""########################################################################################
Name: api_engine/api_engine.py
Description: The api engine is the core class of this project.
This engine will manage all the sub - components and is responsible for the main loop
Imports:
"""

from typing import List

from fastapi import APIRouter

from ..globals import *
from .api_engine_base import API_Engine_Base
from .class_functions import init, run, stop

# from threading import Thread
"""
########################################################################################"""


class API_Engine(API_Engine_Base):
    # define class variables
    app = None
    routes: List[APIRouter] = []
    config = None
    uvicorn_server = None
    uvicorn_thread = None

    def __init__(self, *args, **kwargs):
        init(self, *args, **kwargs)

    def run(self, *args, **kwargs):
        run(self, *args, **kwargs)

    def stop(self, *args, **kwargs):
        stop(self, *args, **kwargs)
