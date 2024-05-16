"""########################################################################################
Name: api_engine/api_engine.py
Description: The api engine is the core class of this project.
This engine will manage all the sub - components and is responsible for the main loop
Imports:
"""

from typing import List

from fastapi import APIRouter

from ..globals import *
from .functions import *

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

    def __init__(self):
        init(self)

    def run(self):
        run(self)

    def stop(self):
        stop(self)
