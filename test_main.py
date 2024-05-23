"""########################################################################################
Name: test_main.py
Description: This will start the test run going through all API endpoints
and looking for possible errors 
Imports:
"""

import os

os.environ["SETTINGS_VARIATION_PATH"] = "./project-settings-test.json"
from logging.handlers import TimedRotatingFileHandler
from time import sleep

import package as p
import package.tests as tests
from package.utils.classes.test_client import CustomTestClient

"""
########################################################################################"""


# create a test client with the given FastAPI app
# The process is similar to the one in the main.py file

if __name__ == "__main__":
    # securely grab the app name and the logger streamhandler
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
    p.LOGGER.info(f"Starting the Tests!")
    try:
        api_engine = p.API_Engine()
        api_engine.run(debug=True)

        p.LOGGER.info(f"Starting the Test Client!")
        client = CustomTestClient(api_engine.app, base_url="http://localhost:8000")

        # start the tests
        test_classes = [
            tests.Session_Test(client=client),
            tests.Script_Test(client=client),
        ]

        for test_class in test_classes:
            test_class.test_script()

    except KeyboardInterrupt:
        p.LOGGER.warning(f"Recieved KeyboardInterrupt, stopping gracefully...")
        api_engine.stop()
    except Exception as e:
        p.LOGGER.error(f"An error occured:\n{e}")
        api_engine.stop()

    # say a final goodbye
    p.LOGGER.info(f"Stopping Tests!")
