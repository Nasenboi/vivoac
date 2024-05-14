'''########################################################################################
Name: api_engine/api_engine.py
Description: The api engine is the core class of this project.
This engine will manage all the sub - components and is responsible for the main loop
Imports:
'''
# import package globals from ../package/globals.py
from .functions import *
#from fastapi import FastAPI
from ..globals import *
#from threading import Thread
'''
########################################################################################'''


class API_Engine:
    # define class variables
    app = None
    config = None
    uvicorn_server = None
    uvicorn_thread = None
        

    def __init__(self):
        init(self)

    def run(self):
        run(self)

    def stop(self):
        stop(self)