#!/usr/bin/env python3
"""
Flask app module.
"""
from flask import request

from flask import Flask, jsonify, abort
from flask_cors import CORS
import os
from api.v1.views import app_views

app = Flask(__name__)
CORS(app)

app.register_blueprint(app_views)

# Initialize the auth variable
auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")

if AUTH_TYPE:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request():
    """
    Filter each request.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/', '/api/v1/forbidden/']

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error):
    """
    Handler for 401 Unauthorized error.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Handler for 403 Forbidden error.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    app.run(host=host, port=port)
