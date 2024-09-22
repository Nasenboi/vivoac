"""########################################################################################
Name: api_engine/functions.py
Description: This file contains the functions for the API_Engine class in api_engine.py
Imports:
"""

from threading import Thread
from time import sleep

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from uvicorn import Config, Server

from ..globals import *
from ..http_models.base_responses import (
    Response_404,
    Response_422,
    Response_HTTPException,
)
from ..routes import get_api_routes

# Call the function to get the routes
api_routes = get_api_routes()
from ..routes.engine_backend.engine_backend import Engine_Backend
from .routes import API_Engine_Router

api_routes.append(API_Engine_Router)
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


def init(self) -> None:
    LOGGER.debug("api engine - init")
    try:
        self.app = FastAPI(
            responses={404: {"model": Response_404}, 422: {"model": Response_422}}
        )
        self.config = Config(self.app, **SETTINGS_GLOBAL.get("uvicorn-settings"))
        self.uvicorn_server = Server(self.config)
        self.uvicorn_thread = UvicornThread(
            target=self.uvicorn_server.run,
            daemon=True,
            uvicorn_server=self.uvicorn_server,
        )
        # add routes
        self.routes = [route(api_engine=self) for route in api_routes]
        for route in self.routes:
            self.app.include_router(
                route
            )  # more verbose, dependencies=[Depends(log_request_info)]

        # Exception Handlers
        self.app.add_exception_handler(404, exception_handler_404)
        self.app.add_exception_handler(422, exception_handler_422)
        self.app.add_exception_handler(HTTPException, exception_handler)

        self.uvicorn_thread.setDaemon(True)

        self.engine_backend = Engine_Backend()
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


# -- Exception Handlers --
async def exception_handler_404(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content=Response_404().model_dump(),
    )


async def exception_handler_422(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=Response_422(exc).model_dump(),
    )


async def exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=Response_HTTPException(exc).model_dump(),
    )
