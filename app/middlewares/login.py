from functools import wraps

# Database ORMs
from db import db, User, email_len, password_len

import json
from datetime import datetime, timedelta
import jwt
from flask import request, jsonify, make_response
from app import app, Login


# decorator for verifying the user
def login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # creates dictionary of form auth data
        auth = request.form

        # returns 400 if any email or / and password is missing
        if not auth or not auth.get("email") or not auth.get("password"):
            return make_response("Email or password is missing!", 400)

        email = auth.get("email")
        password = auth.get("password")

        response = Login.run(inputs={"email": email, "password": password})

        is_login = response.get("result").get("login")
        return f(is_login, *args, **kwargs)

    return decorated
