#!/usr/bin/env python3
"""route config
"""


from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def main():
    """basic route config"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def user():
    """check for registered users"""
    mail = request.form.get('email')
    passcode = request.form.get('password')
    try:
        AUTH.register_user(email=mail, password=passcode)
        return jsonify({"email": f"{mail}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """user login route"""
    email = request.form.get('email')
    password = request.form.get('password')
    validate = AUTH.valid_login(email=email, password=password)
    if validate is True:
        sessionID = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', sessionID)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """logout route for users"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - The user's profile information.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Return:
        - The user's password reset payload.
    """
    email = request.form.get("email")
    reset_token = None
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
    if reset_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Return:
        - The user's password updated payload.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    is_password_changed = False
    try:
        AUTH.update_password(reset_token, new_password)
        is_password_changed = True
    except ValueError:
        is_password_changed = False
    if not is_password_changed:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
