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
        decoded_64 = decoded_base64_authorization_header
        if (decoded_64 and isinstance(decoded_64, str) and
                ":" in decoded_64):
            res = decoded_64.split(":", 1)
            return (res[0], res[1])
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """object credentials method"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overrides Auth and retrieves User instance for request """
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(b64_header)
        user_creds = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(*user_creds)
