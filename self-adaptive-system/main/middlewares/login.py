# Basic Packages
import os
from functools import wraps
from datetime import datetime, timedelta

# Database ORMs
from main.db import db
from main.db.models.user import User, email_len, password_len

# App Packages
import json
import jwt
from flask import request, make_response
from main import app
from main.modules import Login


# decorator for verifying the user
def user_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # creates dictionary of form auth data
        auth = request.authorization

        # returns 400 if necessary data is missing
        if not auth:
            return make_response("Auth data is missing!", 400)

        response = Login.run(inputs={"email": auth.username, "password": auth.password})

        is_user_login = response.get("result").get("login")

        return f(is_user_login, *args, **kwargs)

    return decorated


# decorator for verifying the admin
def admin_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # creates dictionary of form auth data
        headers = request.headers

        # returns 400 if necessary data is missing
        if not headers:
            return make_response("Headers are missing!", 400)

        admin_secret = headers.get("admin_secret")

        # returns 400 if admin secret is missing
        if not admin_secret:
            return make_response("Admin secret is missing!", 400)

        is_admin_login = admin_secret == os.getenv("ADMIN_SECRET")

        return f(is_admin_login, *args, **kwargs)

    return decorated
