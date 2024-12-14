import os
from functools import wraps
from flask import request, make_response


def admin_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        headers = request.headers
        if not headers:
            return make_response("Headers are missing!", 400)

        admin_secret = headers.get("admin_secret")
        if not admin_secret:
            return make_response("Admin secret is missing!", 400)

        is_admin_login = admin_secret == os.getenv("ADMIN_SECRET")

        return f(is_admin_login, *args, **kwargs)

    return decorated
