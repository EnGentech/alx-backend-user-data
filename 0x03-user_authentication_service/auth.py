#!/usr/bin/env python3
"""Authentication config
"""


import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password"""
    password = password.encode("utf-8")
    hashed_passcode = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_passcode
