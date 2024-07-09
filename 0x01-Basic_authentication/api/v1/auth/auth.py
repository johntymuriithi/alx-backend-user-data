#!/usr/bin/env python3
"""
Module for API authentication management.
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """
    A class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]):
            A list of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path always ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the Authorization
        header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the Authorization header,
            or None if not present.
        """
        if request is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'):
            None, indicating that no user is associated with the request.
        """
        return None
