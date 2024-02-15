#!/usr/bin/env python3
"""Session authentication with expiration
and storage support module for the API.
"""
from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with expiration and storage support.

    This class provides session-based authentication using a database for storage.
    It extends the SessionExpAuth class and adds methods for creating, retrieving,
    and destroying sessions.

    Attributes:
        session_duration (int): The duration of a session in seconds.

    Methods:
        create_session(user_id=None) -> str: Creates and stores a session id for the user.
        user_id_for_session_id(session_id=None) -> str: Retrieves the user id associated with a session id.
        destroy_session(request=None) -> bool: Destroys an authenticated session.
    """
    
    def create_session(self, user_id=None) -> str:
        """Creates and stores a session id for the user.

        Args:
            user_id (str): The id of the user.

        Returns:
            str: The session id.
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Retrieves the user id of the user associated with a given session id.

        Args:
            session_id (str): The session id.

        Returns:
            str: The user id associated with the session id.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session.

        Args:
            request (object): The request object.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
