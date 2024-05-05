'''########################################################################################
The api engine is the core class of this project.
This engine will manage all the sub - components and is responsible for the main loop

########################################################################################'''
# import package globals from ../package/globals.py
from .functions import *

class ApiEngine:
    def __init__(self):
        init(self)

    def run(self):
        run(self)

    def stop(self):
        stop(self)