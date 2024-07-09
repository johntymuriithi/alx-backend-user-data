#!/usr/bin/env python3
"""
BasicAuth module for handling basic authentication.
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Optional, Tuple
from flask import request


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth for basic authentication.
    """
    def extract_base64_authorization_header(self, authorization_header: str)\
            -> Optional[str]:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the Authorization
            header, or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> Optional[str]:
        """
        Decodes the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            base64_authorization_header (str): The Base64 part
            of the Authorization header.

        Returns:
            str: The decoded value as a UTF8 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the user email and password from the decoded Base64 value.

        Args:
            decoded_base64_authorization_header
            (str): The decoded Base64 string.

        Returns:
            tuple: A tuple containing the user email
            and password, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        # Split the decoded string only at the first occurrence of ":"
        parts = decoded_base64_authorization_header.split(':', 1)
        if len(parts) != 2:
            return None, None

        email, password = parts[0], parts[1]
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> (
            Optional)[TypeVar('User')]:
        """
        Returns the User instance based on his email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance, or None if not
             found or invalid credentials.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """
        Retrieves the User instance for a request.

        Args:
            request: The Flask request object.

        Returns:
            User: The User instance, or None if
            not found or invalid credentials.
        """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_authorization_header = (
            self.extract_base64_authorization_header(authorization_header))
        if base64_authorization_header is None:
            return None
        decoded_base64_authorization_header = (
            self.decode_base64_authorization_header
            (base64_authorization_header))
        if decoded_base64_authorization_header is None:
            return None
        user_email, user_pwd = (
            self.extract_user_credentials(decoded_base64_authorization_header))
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
