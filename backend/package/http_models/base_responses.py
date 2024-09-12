"""########################################################################################
Name: http_models/base_responses.py
Description: In here are some dependency functions that will be used for http request parameters.
Imports:
"""

from typing import Dict
from ..globals import SETTINGS_GLOBAL

from .models import VivoacBaseResponse

"""
########################################################################################"""

class Response_404 (VivoacBaseResponse):
    data: Dict = {
        "description": "Not Found",
    }

    def __init__(self):
        super().__init__(data=self.data, api_version=SETTINGS_GLOBAL.get("metadata", {}).get("api_version", "0.0.0"))