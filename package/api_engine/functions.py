'''########################################################################################
To reduce the file size of the class file, all the functions that this class has
and executes are defined here, similar to a ceader and cpp file in c++.

########################################################################################'''
from ..globals import *
from fastapi import FastAPI
from uvicorn import Config, Server
from threading import Thread
from time import sleep

########################################################################################
# inner custom classes

class UvicornThread(Thread):
    def __init__(self, uvicorn_server: Server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uvicorn_server = uvicorn_server

    def run(self):
        self.uvicorn_server.run()


########################################################################################
# class functions


def init(self) -> None:
    LOGGER.debug("api engine - init")
    try:
        self.app = FastAPI()
        self.config = Config(self.app, **SETTINGS_GLOBAL.get("uvicorn-settings"))
        self.uvicorn_server = Server(self.config)
        self.uvicorn_thread = UvicornThread(target=self.uvicorn_server.run,
                                            daemon=True, uvicorn_server=self.uvicorn_server)
        self.uvicorn_thread.setDaemon(True)
    except KeyboardInterrupt:
        # Ignore the KeyboardInterrupt for this
        raise KeyboardInterrupt
    except Exception as e:
        LOGGER.error(f"An error while initializing fastapi:\n{e}")
        raise Warning("Restarting...")


def run(self) -> None:
    LOGGER.debug("api engine - run")
    try:
        LOGGER.debug("api engine - starting uvicorn thread")
        self.uvicorn_thread.start()
        i = 0
        LOGGER.debug("api engine - waiting for uvicorn server to start")
        while not self.uvicorn_server.started and i < 10:
            sleep(1e-3)
            LOGGER.debug("."*i)
            i += 1
        LOGGER.debug("api engine - uvicorn server started successfully")
            
    except KeyboardInterrupt:
        # Ignore the KeyboardInterrupt for this
        raise KeyboardInterrupt
    except Exception as e:
        LOGGER.error(f"An error while running fastapi:\n{e}")
        raise Warning("Restarting...")

    while self.uvicorn_thread.is_alive():
        pass

def stop(self) -> None:
    LOGGER.debug("api engine - stop")
    # stopping uviorn thread
    self.uvicorn_thread.join()
    self.uvicorn_thread = None
    self.uvicorn_server = None
    LOGGER.debug("api engine - uvicorn thread stopped successfully")
