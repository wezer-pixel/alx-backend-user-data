#!/usr/bin/env python3
"""A module for encrypting passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using a random salt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a hashed password was formed from the given password.

    Args:
        hashed_password (bytes): The hashed password to be checked.
        password (str): The password to compare against the hashed password.

    Returns:
        bool: True if the hashed password matches the given password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
