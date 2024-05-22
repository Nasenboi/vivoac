"""########################################################################################
Name: main.py
Description: This file is the first file to be executed when the program is run.
It will set up the next important files: globals and api_engine.
It also handles all exceptions on the top level and tries to keep the program ALIVE!
Imports:
"""

from importlib import reload
from logging.handlers import TimedRotatingFileHandler

import package as p

"""
########################################################################################"""

if __name__ == "__main__":
    # grab the app name and the logger streamhandler
    name = p.SETTINGS_GLOBAL.get("metadata", {}).get("name", "app")
    streamhandler = p.LOGGER.parent.handlers[
        [
            index
            for index, obj in enumerate(p.LOGGER.parent.handlers)
            if isinstance(obj, TimedRotatingFileHandler)
        ][0]
    ]
    streamhandler.doRollover()

    # start the application loop
    p.LOGGER.info(f"Starting {name}, hello world!")
    apiEngine = p.API_Engine()
    apiEngine.run()
    while True:
        try:
            pass
        except KeyboardInterrupt:
            p.LOGGER.warning(f"Recieved KeyboardInterrupt, stopping gracefully...")
            apiEngine.stop()
            break
        except Exception as e:
            p.LOGGER.error(f"An error occured:\n{e}\nRestarting {name}")
            reload(p)
            apiEngine = p.API_Engine()
            apiEngine.run()

    # say a final goodbye
    p.LOGGER.info(f"Stopping {name}, goodbye!")
