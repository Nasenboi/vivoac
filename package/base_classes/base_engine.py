"""########################################################################################
Name: base_classes/base_engine.py
Description: 
Imports:
"""

from typing import Any, Dict

"""
########################################################################################"""


class Base_Engine:
    # class variables:
    pass

    def __init__(self):
        pass

    ############################################################
    # getter functions:

    def get_class_variables(self) -> Dict[str, Any]:
        annotations = self.__annotations__
        for key in annotations.keys():
            annotations[key] = getattr(self, key)
        return annotations

    ############################################################
    # set class variables:

    def set_class_variables(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.__setattr__(key, value)
