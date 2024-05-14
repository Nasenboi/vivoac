'''########################################################################################
Name: utils/decorators.py
Description: This file contains useful decorators for the package.
Imports:
'''

'''
########################################################################################'''



def virtual(func):
    '''This decorator is used to mark a function as a virtual function.
    Virtual functions are functions that are meant to be overridden by subclasses.
    If a subclass does not override a virtual function, an error will be raised when the function is called.'''
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f'The function {func.__name__} is a virtual function and must be overridden by a subclass.')
    return wrapper