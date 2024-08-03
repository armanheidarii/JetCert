# Database ORMs
from db import db, User, email_len, password_len

from flask import request, jsonify, make_response
from app import app
from app.middlewares.login import login


# User Database Route
# this route sends back list of users
@app.route("/users", methods=["GET"])
@login
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
        # to the response list
        output.append(
            {"public_id": user.public_id, "name": user.name, "email": user.email}
        )

    return jsonify({"users": output})
