"""########################################################################################
Name: api_engine/functions.py
Description: This file contains the functions for the API_Engine class in api_engine.py
Imports:
"""

from threading import Thread
from time import sleep

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_sessions.backends.implementations import InMemoryBackend
from uvicorn import Config, Server

from ..globals import *
from ..routes import *
from .routes import API_Engine_Router

"""
########################################################################################"""


########################################################################################
# Inner custom classes


class UvicornThread(Thread):
    def __init__(self, uvicorn_server: Server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uvicorn_server = uvicorn_server

    def run(self):
        self.uvicorn_server.run()


########################################################################################
# Class functions


########################################
# Essentials:


async def log_request_info(request: Request):
    try:
        request_body = await request.json()
    except Exception:
        return

    LOGGER.info(
        f"{request.method} request to {request.url} metadata\n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {request_body}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
        f"\tCookies: {request.cookies}\n"
    )


def init(self) -> None:
    LOGGER.debug("api engine - init")
    try:
        self.app = FastAPI()
        self.config = Config(self.app, **SETTINGS_GLOBAL.get("uvicorn-settings"))
        self.uvicorn_server = Server(self.config)
        self.uvicorn_thread = UvicornThread(
            target=self.uvicorn_server.run,
            daemon=True,
            uvicorn_server=self.uvicorn_server,
        )
        # add routes
        self.routes = [
            API_Engine_Router(api_engine=self),
            Session_Router(api_engine=self),
            Audio_Router(api_engine=self),
            AI_API_Handler_Router(api_engine=self),
            Script_Router(api_engine=self),
        ]
        for route in self.routes:
            self.app.include_router(
                route
            )  # more verbose, dependencies=[Depends(log_request_info)]

        self.uvicorn_thread.setDaemon(True)

        self.session_backend = InMemoryBackend()
    except KeyboardInterrupt:
        # Ignore the KeyboardInterrupt for this
        raise KeyboardInterrupt
    except Exception as e:
        LOGGER.error(f"An error while initializing fastapi:\n{e}")
        raise Warning("Restarting...")


def run(self, debug: bool = False) -> None:
    LOGGER.debug("api engine - run")
    try:
        LOGGER.debug("api engine - starting uvicorn thread")
        self.uvicorn_thread.start()
        i = 0
        LOGGER.debug("api engine - waiting for uvicorn server to start")
        while not self.uvicorn_server.started:
            sleep(1e-3)
            LOGGER.debug("." * i)
            i += 1
            if i > 3:
                i = 0
        LOGGER.debug("api engine - uvicorn server started successfully")

        while self.uvicorn_thread.is_alive() and not debug:
            pass

    except KeyboardInterrupt:
        # Ignore the KeyboardInterrupt for this
        raise KeyboardInterrupt
    except Exception as e:
        LOGGER.error(f"An error while running fastapi:\n{e}")
        raise Warning("Restarting...")


def stop(self) -> None:
    LOGGER.debug("api engine - stop")
    # stopping uviorn server
    self.uvicorn_server.should_exit = True
    self.uvicorn_server = None
    # and then the thread
    self.uvicorn_thread.join()
    self.uvicorn_thread = None
    LOGGER.debug("api engine - uvicorn thread stopped successfully")
