"""########################################################################################
Name: engine_backend/engine_backend.py
Description: 
Imports:
"""

from typing import List

from ...modules import *
from .models import *

"""
########################################################################################"""


class Engine_Backend:
    session_sub_engines: List[API_Sub_Engines] = []

    def add_session_engines(self, session_id: str | int):
        self.session_sub_engines.append(API_Sub_Engines(session_id=session_id))

    def get_session_engines(self, session_id: str | int) -> API_Sub_Engines:
        for session in self.session_sub_engines:
            if session.session_id == session_id:
                return session

    def close_session_engines(self, session_id: str | int) -> str | int:
        for session in self.session_sub_engines:
            if session.session_id == session_id:
                self.session_sub_engines.remove(session)
                return session_id
