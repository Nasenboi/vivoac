'''########################################################################################
The api engine is the core class of this project.
This engine will manage all the sub - components and is responsible for the main loop

########################################################################################'''
# import package globals from ../package/globals.py
from .functions import *
from fastapi import FastAPI

class ApiEngine:
    # define class variables
    app = FastAPI()

    def __init__(self):
        init(self)

    def run(self):
        run(self)

    def stop(self):
        stop(self)