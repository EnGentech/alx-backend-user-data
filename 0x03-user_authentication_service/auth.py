#!/usr/bin/env python3
"""Authentication config
"""


import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash password"""
    password = password.encode("utf-8")
    hashed_passcode = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_passcode


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """class instance init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """user registration for basic auth"""
        try:
            response = self._db.find_user_by(email=email)
            if response:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashPasscode = _hash_password(password)
            self._db.add_user(email, hashPasscode)