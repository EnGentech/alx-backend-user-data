#!/usr/bin/env python3
""" API authorization file
"""


from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
import os


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    """login route"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({ "error": "email missing" }), 400
    if not password:
        return jsonify({ "error": "password missing" }), 400
    user = User.search({"email": email})
   
    if user:
        for usser in user:
            if usser.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(usser.id)
                resp = jsonify(usser.to_json())
                session_name = os.getenv('SESSION_NAME')
                resp.set_cookie(session_name, session_id)
                return resp
        else:
            return jsonify({ "error": "wrong password" }), 401
    else:
        return jsonify({ "error": "no user found for this email" }), 404
