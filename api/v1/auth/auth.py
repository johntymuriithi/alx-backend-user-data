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

    def require_auth(self, path: str, excluded_paths: List[str]) \
            -> bool:
        """
        Checks if authentication is required for a
         given path based on excluded paths.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List
            of paths to exclude from authentication.

        Returns:
            bool: True if authentication is required,
             False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return False

        # Check each excluded path
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                # Remove the '*' from the end to match prefixes
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
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
