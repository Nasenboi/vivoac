"""########################################################################################
Name: user/dependencies.py
Description: 
Imports:
"""

import json
import os
from typing import Dict

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pymongo.collection import Collection

from ...db import OAUTH_2_SCHEME
from ...globals import LOGGER, SETTINGS_GLOBAL

"""
########################################################################################"""
