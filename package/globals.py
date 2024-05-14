'''########################################################################################
In here are all the global variables and objects that are used throughout the project.

########################################################################################'''

# Imports
import json
import logging.config
import colorlog
import os


# Firstly load the settings for the project, they should be in a json file
# and most of the settings are globals anyway so lets read them in here
# Please read the documentation on what variables the settings file could contain
if "PROJECT_SETTINGS_PATH" in os.environ:
    PROJECT_SETTINGS_PATH = os.environ["PROJECT_SETTINGS_PATH"]
else:
    PROJECT_SETTINGS_PATH = "./project-settings.json"

def load_project_settings() -> dict:
    with open(PROJECT_SETTINGS_PATH, "r") as file:
        return json.load(file)
SETTINGS_GLOBAL = load_project_settings()


# Logger with its config:
# create log file if it does not exist, logger will get angry if it does not exist
filename = SETTINGS_GLOBAL.get("logging-config")["handlers"]["file"]["filename"]
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    pass
logging.config.dictConfig(SETTINGS_GLOBAL.get("logging-config"))
LOGGER = colorlog.getLogger("main")