from flask import request, make_response

from main.db.models import User
from main import app


@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    if not data:
        return make_response("Data is missing!", 400)

    email, name = data.get("email"), data.get("name")
    password = data.get("password")
    if not email or not password:
        return make_response("Email or password is missing!", 400)

    if len(email) > User.email.max_length:
        return make_response("Your email is invalid!", 400)

    if len(password) > User.password.max_length:
        return make_response("Your password is invalid!", 400)

    if len(name) > User.name.max_length:
        return make_response("Your name is invalid!", 400)

    try:
        user = User.query.filter_by(email=email).first()
        return make_response("User already exists. Please Log in.", 202)

    except Exception as e:
        pass

    user = User.create(name=name, email=email, password=password)
    return make_response("Successfully registered.", 201)
