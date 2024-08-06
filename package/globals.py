"""########################################################################################
In here are all the global variables and objects that are used throughout the project.



Imports:
"""

import json
import logging.config
import os
from typing import Dict

import colorlog
from pymongo import MongoClient
from pymongo.collection import Collection

from .utils.functions import json_update

"""
########################################################################################"""


# Firstly load the settings for the project, they should be in a json file
# and most of the settings are globals anyway so lets read them in here
# Please read the documentation on what variables the settings file could contain
PROJECT_SETTINGS_PATH = "./project-settings.json"


if "SETTINGS_VARIATION_PATH" in os.environ:
    SETTINGS_VARIATION_PATH = os.environ["SETTINGS_VARIATION_PATH"]


def load_project_settings() -> dict:
    with open(PROJECT_SETTINGS_PATH, "r") as file:
        settings = json.load(file)

    if "SETTINGS_VARIATION_PATH" in globals():
        with open(SETTINGS_VARIATION_PATH, "r") as file:
            settings_variation = json.load(file)
        settings = json_update(settings, settings_variation)

    return settings


SETTINGS_GLOBAL = load_project_settings()


# Logger with its config:
# create log file if it does not exist, logger will get angry if it does not exist
filename = SETTINGS_GLOBAL.get("logging-config")["handlers"]["file"]["filename"]
os.makedirs("/".join(filename.split("/")[:-1]), exist_ok=True)
with open(filename, "w") as f:
    pass
logging.config.dictConfig(SETTINGS_GLOBAL.get("logging-config"))
LOGGER = colorlog.getLogger("main")

# Create the other directories that are needed, if they dont exist:
directories = SETTINGS_GLOBAL.get("directories")
for directory in directories.values():
    os.makedirs(directory, exist_ok=True)

# Create the client for the mongo database:
DB_CLIENT = MongoClient(SETTINGS_GLOBAL.get("database", {}).get("url", None))
db_name = SETTINGS_GLOBAL.get("database", {}).get("collection", "vivoac")
VIVOAC_DB = DB_CLIENT[db_name]

# Initialize and create the collections if they dont exist:
DB_COLLECTIONS: Dict[str, Collection] = {
    "sessions": None,
    "users": None,
    "voices": None,
    "voice_talents": None,
}
for collection in DB_COLLECTIONS.keys():
    DB_COLLECTIONS[collection] = VIVOAC_DB[collection]
