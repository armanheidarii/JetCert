import os
from functools import wraps
from flask import request, make_response

from main.modules import Login


def user_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return make_response("Auth data is missing!", 400)

        response = Login.run(
            inputs={"email": auth.username, "password": auth.password}
        ).get("result")

        is_user_login = response.get("login")

        return f(is_user_login, *args, **kwargs)

    return decorated
