'''########################################################################################
In here are all the global variables and objects that are used throughout the project.

########################################################################################'''

# Imports
import json
import logging.config
import colorlog


# Firstly load the settings for the project, they should be in a json file
# and most of the settings are globals anyway so lets read them in here
# Please read the documentation on what variables the settings file could contain
PROJECT_SETTINGS_PATH = "./project-settings.json"
def load_project_settings() -> dict:
    with open(PROJECT_SETTINGS_PATH, "r") as file:
        return json.load(file)
SETTINGS_GLOBAL = load_project_settings()


# Logger with its config:
logging.config.dictConfig(SETTINGS_GLOBAL.get("logging-config"))
LOGGER = colorlog.getLogger("main")
