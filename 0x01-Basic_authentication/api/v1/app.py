#!/usr/bin/env python3
"""
Main app for the API.
"""

from flask import Flask, jsonify
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(401)
def unauthorized_error_handler(error):
    """
    Error handler for 401 Unauthorized.

    Returns:
        A JSON response with an error message and a 401 status code.
    """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden_error_handler(error):
    """
    Error handler for 403 Forbidden.

    Returns:
        A JSON response with an error message and a 403 status code.
    """
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    app.run(host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", "5000")))
