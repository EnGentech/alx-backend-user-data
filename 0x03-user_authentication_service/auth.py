#!/usr/bin/env python3
"""Authentication config
"""


import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """hash password"""
    password = password.encode("utf-8")
    hashed_passcode = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_passcode


def _generate_uuid() -> str:
    """return a string representation of uuid"""
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """validate user"""
        try:
            response = self._db.find_user_by(email=email)
            if response:
                encodePassword = password.encode("utf-8")
                if bcrypt.checkpw(encodePassword, response.hashed_password):
                    return True
                else:
                    return False
        except Exception:
            return False

    def create_session(self, email: str):
        """create a session_id for a user"""
        try:
            response = self._db.find_user_by(email=email)
            response.session_id = _generate_uuid()
            self._db._session.commit()
            return response.session_id
        except Exception:
            return
