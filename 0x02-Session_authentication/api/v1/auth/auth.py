#!/usr/bin/env python3
"""Authentication module for the API.
"""
import os
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class.

    This class provides methods for authentication and authorization.

    Methods:
        require_auth(path: str, excluded_paths: List[str]) -> bool:
            Checks if a path requires authentication.

        authorization_header(request=None) -> str:
            Gets the authorization header field from the request.

        current_user(request=None) -> TypeVar('User'):
            Gets the current user from the request.

        session_cookie(request=None) -> str:
            Gets the value of the cookie named SESSION_NAME.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header field from the request.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Gets the value of the cookie named SESSION_NAME.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
