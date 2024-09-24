"""########################################################################################
Name: test_main.py
Description: This will start the test run going through all API endpoints
and looking for possible errors 
Imports:
"""

import os

os.environ["SETTINGS_VARIATION_PATH"] = "./project-settings-test.json"
import json
from logging.handlers import TimedRotatingFileHandler

import package as p
from package.tests import get_test_classes

test_classes = get_test_classes()
from package.db import ADMIN_PASSWORD, ADMIN_USER, DB_COLLECTIONS
from package.utils.classes.test_client import CustomTestClient

"""
########################################################################################"""


# create a test client with the given FastAPI app
# The process is similar to the one in the main.py file

if __name__ == "__main__":
    # securely grab some important information
    name = p.SETTINGS_GLOBAL.get("metadata", {}).get("name", "app")
    streamhandler = p.LOGGER.parent.handlers[
        [
            index
            for index, obj in enumerate(p.LOGGER.parent.handlers)
            if isinstance(obj, TimedRotatingFileHandler)
        ][0]
    ]
    streamhandler.doRollover()

    test_results = []
    test_result_file = p.SETTINGS_GLOBAL.get("test-settings", {}).get(
        "test_result_file", ""
    )

    test_user = {"username": ADMIN_USER, "password": ADMIN_PASSWORD}

    api_version = p.SETTINGS_GLOBAL.get("metadata", {}).get("api_version", "0.0.0")

    # clearing the database
    p.LOGGER.info(f"Clearing the Database!")
    for collection in DB_COLLECTIONS.keys():
        if collection != "users":
            p.LOGGER.info(f"Clearing the {collection} Collection!")
            DB_COLLECTIONS[collection].delete_many({})

    # start the application loop
    p.LOGGER.info(f"Starting the Tests!")
    try:
        api_engine = p.API_Engine()
        api_engine.run(debug=True)

        p.LOGGER.info(f"Starting the Test Client!")
        client = CustomTestClient(api_engine.app, base_url="http://localhost:8000")

        # authenticate to get a token
        p.LOGGER.info(f"Authenticating the Test User!")
        response = client.post("/token", data=test_user)
        token = response.json().get("access_token")

        test_kwargs = {
            "client": client,
            "test_user": test_user,
            "token": token,
            "api_version": api_version,
        }

        # start the tests
        for test_class in test_classes:
            result = test_class(**test_kwargs).test_script()
            # alt formatting
            # test_results.append({"test_class": test_class.__name__, "results": result})
            test_results.extend(result)

        # store the tesults in a file:
        if test_result_file != "":
            p.LOGGER.info(f"Storing the test results in {test_result_file}")

            with open(test_result_file, "w") as file:
                json.dump(test_results, file, indent=4)

    except KeyboardInterrupt:
        p.LOGGER.warning(f"Recieved KeyboardInterrupt, stopping gracefully...")
        api_engine.stop()
    except Exception as e:
        p.LOGGER.error(f"An error occured:\n{e}")
        api_engine.stop()

    # say a final goodbye
    p.LOGGER.info(f"Stopping Tests!")
