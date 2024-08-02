"""########################################################################################
Name: utils/decorators.py
Description: This file contains useful decorators for the package.
Imports:
"""

from functools import wraps

from ..globals import LOGGER

"""
########################################################################################"""


def virtual(func):
    """This decorator is used to mark a function as a virtual function.
    Virtual functions are functions that are meant to be overridden by subclasses.
    If a subclass does not override a virtual function, an error will be raised when the function is called.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(
            f"The function {func.__name__} is a virtual function and must be overridden by a subclass."
        )

    return wrapper


def session_fetch(func):
    """
    Depricated! use package/routes/ai_api_handler/routes.py fetch_session function instead!
    This decorator is used to fetch a session object from the session_id parameter.
    The session object is then passed to the decorated function as a keyword argument.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        session_id = kwargs.get("session_id", "")
        session = await args[0].api_engine.session_backend.read(session_id=session_id)
        kwargs["session"] = session
        return await func(*args, **kwargs)

    return wrapper
