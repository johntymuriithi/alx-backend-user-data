#!/usr/bin/env python3
"""
API views for the basic authentication project.
"""

from flask import Blueprint, jsonify, abort

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns the status of the API.

    Returns:
        A JSON response with the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized():
    """
    Raises a 401 Unauthorized error.

    This endpoint is used to test the custom
    error handler for 401 Unauthorized.
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden():
    """
    Raises a 403 Forbidden error.

    This endpoint is used to test the custom error handler for 403 Forbidden.
    """
    abort(403)
