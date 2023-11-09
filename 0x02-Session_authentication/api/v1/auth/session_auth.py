#!/usr/bin/env python3
""" API authorization file
"""


from api.v1.auth.auth import Auth
from uuid import uuid4
from api.v1.views import User


class SessionAuth(Auth):
    """class definition"""
    user_id_by_session_id = {}

    def create_session(
            self, user_id: str = None) -> str:
        """class instance method"""
        if user_id is None \
                or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> str:
        """session id"""
        if session_id is None \
                or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """current user validation"""
        key = self.session_cookie(request)
        obtained = self.user_id_for_session_id(key)
        return User.get(obtained)
    
    def destroy_session(self, request=None):
        """destroy the active user session"""
        if request is None:
            return False
        session_value = self.session_cookie(request)
        if not session_value:
            return False
        session_user_id = self.user_id_for_session_id(session_value)
        if session_user_id is None:
            return False
        del self.user_id_by_session_id["session_value"]
