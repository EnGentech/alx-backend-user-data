#!/usr/bin/env python3
""" API authorization file
"""


from flask import request
from typing import List, TypeVar
import os


class Auth:
    """class definition"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        return False for now
        """
        if path is None or not excluded_paths:
            return True
        for i in excluded_paths:
            if i.endswith('*') and path.startswith(i[:-1]):
                return False
            elif i in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        return None for now
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        return None for now
        """
        if request is None:
            return None

    def session_cookie(self, request=None):
        """return cookies from request"""
        if request is None:
            return None
        cookie = os.getenv("_my_session_id")
