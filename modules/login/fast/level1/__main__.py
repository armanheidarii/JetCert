import sys

sys.path.append(".")

import json

# from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from db import User, email_len, password_len


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_json_inputs():
    return json.loads(input())


inputs = get_json_inputs()

email = inputs.get("email")
password = inputs.get("password")

if len(email) > email_len:
    print(json.dumps({"login": False}))
    eprint("Your email is invalid!")
    exit(0)

if len(password) > password_len:
    print(json.dumps({"login": False}))
    eprint("Your email is invalid!")
    exit(0)

with app.app_context():
    user = User.query.filter_by(email=email).first()

if not user:
    print(json.dumps({"login": False}))
    eprint("The user with the given email address was not found!")
    exit(0)

# if check_password_hash(user.password, auth.get("password")):
if user.password != password:
    print(json.dumps({"login": False}))
    eprint("Your password was not match!")
    exit(0)

print(json.dumps({"login": True}))
