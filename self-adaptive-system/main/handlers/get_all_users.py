# Database ORMs
from main.db import db
from main.db.models.user import User

# App Packages
from flask import request, make_response
from main import app
from main.middlewares.login import admin_login
from main.modules import Crypto


@app.route("/users", methods=["GET"])
@admin_login
def get_all_users(is_login):

    if not is_login:
        return make_response("Unauthorized", 401)

    # querying the database
    # for all the entries in it
    users = User.query.all()

    # converting the query objects
    # to list of jsons
    output = []

    for user in users:
        # appending the user data json
        # to the response list by encrypted email
        output.append(
            {
                "public_id": user.public_id,
                "name": user.name,
                "email": Crypto.run(inputs={"plaintext": user.email}).get("result"),
            }
        )

    return {"users": output}
