import json
from flask import request, make_response

from main import app
from main.middlewares.user_login import user_login
from main.modules import Physics, Crypto


@app.route("/lennard-jones", methods=["GET"])
@user_login
def lennard_jones(is_login):
    if not is_login:
        return make_response("Unauthorized", 401)

    data = request.form
    if not data:
        return make_response("Data is missing!", 400)

    try:
        cluster = json.loads(data.get("cluster"))

    except:
        return make_response("Necessary data is in an invalid form!", 400)

    if not cluster:
        return make_response("Physics data is missing!", 400)

    response = Physics.run(inputs={"cluster": cluster}).get("result")

    energy = response.get("energy")

    return make_response(
        {"energy": Crypto.run(inputs={"plaintext": energy}).get("result")},
        200,
    )
