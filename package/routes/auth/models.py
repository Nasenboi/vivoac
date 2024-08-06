"""########################################################################################
Name: auth/models.py
Description: 
Imports:
"""

from pydantic import BaseModel

"""
########################################################################################"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    id: int | str = None
