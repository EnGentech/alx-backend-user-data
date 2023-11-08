#!/usr/bin/env python3
""" API authorization file
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """class definition"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        return False for now
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            path = path + '/'
        for route in excluded_paths:
            if not route.endswith('/'):
                route = route + '/'
        return False if path in excluded_paths else True

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
