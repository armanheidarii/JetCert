from flask import request, make_response

from main.db.models.user import UserModel
from main import app
from main.middlewares.admin_login import admin_login
from main.modules import Crypto


@app.route("/users", methods=["GET"])
@admin_login
def get_all_users(is_login):
    if not is_login:
        return make_response("Unauthorized", 401)

    users = UserModel.select()

    outputs = []
    for user in users:
        outputs.append(
            {
                "public_id": user.public_id,
                "name": user.name,
                "email": Crypto.run(inputs={"plaintext": user.email}).get("result"),
            }
        )

    return make_response({"users": outputs}, 200)
