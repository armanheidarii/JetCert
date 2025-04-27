from flask import request, make_response

from main.db.models import User
from main import app
from main.middlewares import admin_login


@app.route("/users/<string:email>", methods=["DELETE"])
@admin_login
def delete_user(is_login, email):
    if not is_login:
        return make_response("Unauthorized", 401)

    try:
        user = User.get(User.email == email)
        user.delete_instance()
        return make_response("User deleted successfully", 200)

    except Exception as e:
        return make_response("User not found", 404)
