"""########################################################################################
Name: http_models/base_responses.py
Description: In here are some dependency functions that will be used for http request parameters.
Imports:
"""

from typing import Any, Dict, Optional

from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import BaseModel

from .models import VivoacBaseResponse

"""
########################################################################################"""


class Response_HTTPException(VivoacBaseResponse[Dict[str, Any]]):
    # generic error
    def __init__(self, exc: HTTPException):
        data: Dict[str, Any] = {
            "detail": exc.detail,
        }
        super().__init__(
            data=data,
        )


class Response_404(VivoacBaseResponse[Dict[str, str]]):
    # not found errors
    data: Dict[str, str] = {
        "description": "Not Found",
    }


class Validation_Error_Details(BaseModel):
    loc: Optional[str]
    msg: Optional[str]
    type: Optional[str]


class Response_422(VivoacBaseResponse[Validation_Error_Details]):
    # validation errors
    def __init__(self, exc: RequestValidationError):
        data: Validation_Error_Details = Validation_Error_Details(
            loc=exc.loc,
            msg=exc.msg,
            type=exc.type,
        )
        super().__init__(data=data)
