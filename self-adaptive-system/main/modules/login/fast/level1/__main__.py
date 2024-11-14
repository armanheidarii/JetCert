import os
import json
import sqlite3


email_len = 70
password_len = 80


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

db_path = os.getenv("DB_URI")
connection = sqlite3.connect(db_path)
cur = connection.cursor()

user = cur.execute("SELECT * from User WHERE Email = ?", [email]).fetchone()

if not user:
    print(json.dumps({"login": False}))
    eprint("The user with the given email address was not found!")
    exit(0)

if user[4] != password:
    print(json.dumps({"login": False}))
    eprint("Your password was not match!")
    exit(0)

print(json.dumps({"login": True}))






connection.close()
