import os
import sys
import json
from dotenv import load_dotenv
from peewee import SqliteDatabase
from playhouse.reflection import generate_models, print_model, print_table_sql


load_dotenv()

db_path = os.getenv("DB_PATH")
db = SqliteDatabase(db_path)
models = generate_models(db)
User = models.get("user")


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_json_inputs():
    return json.loads(input())


inputs = get_json_inputs()

email = inputs.get("email")
password = inputs.get("password")

if len(email) > User.email.max_length:
    print(json.dumps({"login": False}))
    eprint("Your email is invalid!")
    exit(0)

if len(password) > User.password.max_length:
    print(json.dumps({"login": False}))
    eprint("Your email is invalid!")
    exit(0)

user = None
try:
    user = User.get(User.email == email)

except Exception as e:
    print(json.dumps({"login": False}))
    eprint("The user with the given email address was not found!")
    exit(0)

if user.password != password:
    print(json.dumps({"login": False}))
    eprint("Your password was not match!")
    exit(0)

print(json.dumps({"login": True}))
