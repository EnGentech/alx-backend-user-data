#!/usr/bin/env python3
""" API authorization file
"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """class definition"""
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """class method definition"""
        if authorization_header is None or \
            type(authorization_header) is not str \
                or not authorization_header.startswith("Basic "):
            return None
        else:
            basic, authenticator = authorization_header.split()
            return authenticator
