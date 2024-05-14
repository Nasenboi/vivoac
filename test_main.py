'''########################################################################################
Name: tests/test_main.py
Description: This will start the test run going through all API endpoints
and looking for possible errors 
Imports:
'''
import os
os.environ["SETTINGS_VARIATION_PATH"] = "./project-settings-test.json"
from fastapi.testclient import TestClient
import package as p
from logging.handlers import  TimedRotatingFileHandler 
'''
########################################################################################'''


# create a test client with the given FastAPI app
# The process is similar to the one in the main.py file

if __name__ == "__main__":
    # securely grab the app name and the logger streamhandler
    name = p.SETTINGS_GLOBAL.get("metadata", {}).get("name", "app")
    streamhandler = p.LOGGER.parent.handlers[ [index for index, obj in enumerate(p.LOGGER.parent.handlers) if isinstance(obj, TimedRotatingFileHandler)][0]]
    streamhandler.doRollover()
    
    # start the application loop
    p.LOGGER.info(f"Starting the Tests!")
    try:
        apiEngine = p.API_Engine()
        apiEngine.run()

        TestClient(
            apiEngine.app,
            base_url="http://localhost:8000"
        )


    except KeyboardInterrupt:
        p.LOGGER.warning(f"Recieved KeyboardInterrupt, stopping gracefully...")
        apiEngine.stop()
    except Exception as e:
        p.LOGGER.error(f"An error occured:\n{e}")
        apiEngine.stop()

    # say a final goodbye
    p.LOGGER.info(f"Stopping Tests!")