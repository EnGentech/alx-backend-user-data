#!/usr/bin/env python3
"""route config
"""


from flask import Flask, jsonify, request, abort, make_response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
