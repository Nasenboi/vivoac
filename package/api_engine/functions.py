'''########################################################################################
To reduce the file size of the class file, all the functions that this class has
and executes are defined here, similar to a ceader and cpp file in c++.

########################################################################################'''
from package.globals import *
from fastapi import FastAPI
import uvicorn

def init(self) -> None:
    LOGGER.debug("api engine - init")
    uvicorn.run(self.app, **SETTINGS_GLOBAL.get("uvicorn-settings"))


def run(self) -> None:
    LOGGER.debug("api engine - run")

def stop(self) -> None:
    LOGGER.debug("api engine - stop")