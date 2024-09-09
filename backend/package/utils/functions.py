"""########################################################################################
Name: utils/functions.py
Description: This file contains useful functions that are used throughout the project.
Imports:
"""

from fastapi import HTTPException, Request

from .. import globals

"""
########################################################################################"""


def json_update(json_obj: dict, new_json_obj: dict) -> dict:
    """
    This function will update each field in the json object with the given fields of the new json object.
    :param json_obj: The json object to update
    :param new_json_obj: The new json object
    :return: The updated json object
    """

    def update_or_recursion(current_obj: dict, new_obj: dict):
        for key, value in new_obj.items():
            if isinstance(value, dict):
                # If the value is a dictionary, recurse to update nested objects
                if key in current_obj and isinstance(current_obj[key], dict):
                    update_or_recursion(current_obj[key], value)
                else:
                    current_obj[key] = value
            else:
                # Update fields
                current_obj[key] = value

    update_or_recursion(json_obj, new_json_obj)

    return json_obj


async def fetch_session(api_engine: object, session_id: str):
    """
    This function will fetch a session object with the given session_id from the api_engine.
    :param api_engine: The api_engine
    :param session_id: The session id
    :return session: The session object
    """
    session = None
    try:
        session = await api_engine.session_backend.read(session_id=session_id)
        return session
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Session with id {session_id} not found: {e}"
        )


async def log_request_info(request: Request):
    try:
        request_body = await request.json()
    except Exception:
        return

    globals.LOGGER.info(
        f"{request.method} request to {request.url} metadata\n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {request_body}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
        f"\tCookies: {request.cookies}\n"
    )
