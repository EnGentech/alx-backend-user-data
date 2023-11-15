#!/usr/bin/env python3
"""route config
"""


from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
