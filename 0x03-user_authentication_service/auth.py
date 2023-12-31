#!/usr/bin/env python3
"""Authentication config
"""


import bcrypt
from typing import Union
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

    def create_session(self, email: str) -> str:
        """create a session_id for a user"""
        try:
            response = self._db.find_user_by(email=email)
            response.session_id = _generate_uuid()
            self._db._session.commit()
            return response.session_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> User:
        """A method that return a user base on session_id"""
        try:
            find = self._db.find_user_by(session_id=session_id)
            return find
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """destroy a session_id"""
        if user_id:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given the user's reset token.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
