#!/usr/bin/env python3
"""The `user` model's module.

This module defines the `User` class, which represents a record from the `users` table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """Represents a record from the `user` table.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str): The session ID of the user.
        reset_token (str): The reset token of the user.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
