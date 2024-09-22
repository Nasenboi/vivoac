"""########################################################################################
Name: utils/decorators.py
Description: This file contains useful decorators for the package.
Imports:
"""

from functools import wraps

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


# TODO maybe add a decorator as an endpoint wrapper to handle exceptions and return a proper error response
