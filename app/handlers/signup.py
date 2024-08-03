# Database ORMs
from db import db, User, name_len, email_len, password_len

# App Packages
import uuid
from flask import request, jsonify, make_response
from app import app

# from werkzeug.security import generate_password_hash, check_password_hash


# signup route
@app.route("/signup", methods=["POST"])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # returns 400 if any email or / and password is missing
    if not data or not data.get("email") or not data.get("password"):
        return make_response("Email or password is missing!", 400)

    # gets name, email and password
    name, email = data.get("name"), data.get("email")
    password = data.get("password")

    # returns 400 if the user does not send the data according to the rules
    if len(name) > name_len:
        return make_response("Your name is invalid!", 400)

    if len(email) > email_len:
        return make_response("Your email is invalid!", 400)

    if len(password) > password_len:
        return make_response("Your password is invalid!", 400)

    # checking for existing user
    user = User.query.filter_by(email=email).first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            # password=generate_password_hash(password),
            password=password,
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        # returns 201 if user is created successfully
        return make_response("Successfully registered.", 201)
    else:
        # returns 202 if user already exists
        return make_response("User already exists. Please Log in.", 202)
