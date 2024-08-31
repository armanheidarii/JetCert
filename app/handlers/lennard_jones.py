# App Packages
import json
from flask import request, jsonify, make_response
from app import app, Physics, Crypto
from app.middlewares.login import user_login


@app.route("/lennard-jones", methods=["GET"])
@user_login
def lennard_jones(is_login):

    if not is_login:
        return make_response("Unauthorized", 401)

    # creates a dictionary of the form data
    data = request.form

    # returns 400 if necessary data is missing
    if not data:
        return make_response("Data is missing!", 400)

    # gets necessary data
    try:
        cluster = json.loads(data.get("cluster"))

    except:
        return make_response("Necessary data is in an invalid form!")

    # returns 400 if necessary data is missing
    if not cluster:
        return make_response("Physics data is missing!", 400)

    response = Physics.run(inputs={"cluster": cluster}).get("result")

    energy = response.get("energy")

    return {"energy": Crypto.run(inputs={"plaintext": energy}).get("result")}
