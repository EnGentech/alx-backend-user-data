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
        return False

    def authorization_header(self, request=None) -> str:
        """
        return None for now
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        return None for now
        """
        return None