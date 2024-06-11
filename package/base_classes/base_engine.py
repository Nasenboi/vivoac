"""########################################################################################
Name: base_classes/base_engine.py
Description: 
Imports:
"""

"""
########################################################################################"""


class Base_Engine:
    # class variables:
    pass

    def __init__(self):
        pass

    ############################################################
    # getter functions:

    def get_class_variables(self):
        annotations = self.__annotations__
        for key in annotations.keys():
            annotations[key] = getattr(self, key)
        return annotations

    ############################################################
    # set class variables:

    def set_class_variables(self, *kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
