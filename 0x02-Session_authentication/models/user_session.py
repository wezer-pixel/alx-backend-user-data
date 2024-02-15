#!/usr/bin/env python3
"""User session module.
"""
from models.base import Base


class UserSession(Base):
    """User session class.

    Attributes:
        user_id (int): The ID of the user associated with the session.
        session_id (str): The ID of the session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a User session instance.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
