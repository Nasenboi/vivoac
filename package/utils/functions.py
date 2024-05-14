'''########################################################################################
Name: utils/functions.py
Description: This file contains useful functions that are used throughout the project.
Imports:
'''
from typing import Any, List
'''
########################################################################################'''

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