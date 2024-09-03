# Database ORMs
from main.db import db
from main.db.models.user import User, email_len, password_len

# App Packages
from flask import request, make_response
from main import app
from main.middlewares.login import admin_login


@app.route("/users/<string:email>", methods=["DELETE"])
@admin_login
def delete_user(is_login, email):

    if not is_login:
        return make_response("Unauthorized", 401)

    user = User.query.filter_by(email=email).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return make_response("User deleted successfully", 200)

    else:
        return make_response("User not found", 404)
