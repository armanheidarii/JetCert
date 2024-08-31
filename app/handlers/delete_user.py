# Database ORMs
from db import db, User, email_len, password_len

# App Packages
from flask import request, make_response
from app import app
from app.middlewares.login import admin_login


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
