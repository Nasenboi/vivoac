'''########################################################################################
To reduce the file size of the class file, all the functions that this class has
and executes are defined here, similar to a ceader and cpp file in c++.

########################################################################################'''
from package.globals import *
import fastapi


def init(self) -> None:
    LOGGER.debug("init")

def run(self) -> None:
    LOGGER.debug("run")

def stop(self) -> None:
    LOGGER.debug("stop")