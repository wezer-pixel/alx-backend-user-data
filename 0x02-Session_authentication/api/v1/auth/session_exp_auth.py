#!/usr/bin/env python3
"""Session authentication with expiration module for the API.
"""
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration.

    This class extends the SessionAuth class and adds the functionality
    of session expiration. It allows creating a session ID for a user
    and retrieving the user ID associated with a given session ID. The
    session ID is stored in a dictionary along with the user ID and the
    creation timestamp. If the session duration is set and the session
    has expired, the user ID will not be returned.

    Attributes:
        session_duration (int): The duration of the session in seconds.
                                If set to 0, the session will not expire.
    """

    def __init__(self) -> None:
        """Initializes a new SessionExpAuth instance.

        The session duration is retrieved from the environment variable
        'SESSION_DURATION'. If the value is not a valid integer, the
        session duration is set to 0.
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session ID for the user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The session ID if successful, None otherwise.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Retrieves the user ID of the user associated with a given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID if the session is valid and has not expired,
                 None otherwise.
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
