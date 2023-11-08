#!/usr/bin/env python3
""" API authorization file
"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """class definition"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """class method definition"""
        if authorization_header is None or \
            type(authorization_header) is not str \
                or not authorization_header.startswith("Basic "):
            return None
        else:
            basic, authenticator = authorization_header.split()
            return authenticator

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decoding method"""
        if base64_authorization_header is None or \
                type(base64_authorization_header) is not str:
            return None
        try:
            obtained = base64.b64decode(base64_authorization_header)
            decodeValue = obtained.decode('utf-8')
            return decodeValue
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """credential extract"""
        if decoded_base64_authorization_header is None or \
                type(decoded_base64_authorization_header) is not str\
                or ":" not in decoded_base64_authorization_header:
            return (None, None)
        else:
            key, value = decoded_base64_authorization_header.split(":")
            return (key, value)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """object credentials method"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None