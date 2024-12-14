from flask import request, make_response

from main.db.models.user import UserModel
from main import app
from main.middlewares.admin_login import admin_login


@app.route("/users/<string:email>", methods=["DELETE"])
@admin_login
def delete_user(is_login, email):
    if not is_login:
        return make_response("Unauthorized", 401)

    try:
        user = UserModel.get(UserModel.email == email)
        user.delete_instance()
        return make_response("User deleted successfully", 200)

    except:
        return make_response("User not found", 404)
