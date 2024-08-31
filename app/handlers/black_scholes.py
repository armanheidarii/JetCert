# App Packages
import json
from flask import request, make_response
from app import app, Finance, Crypto
from app.middlewares.login import user_login


@app.route("/black-scholes", methods=["GET"])
@user_login
def black_scholes(is_login):

    if not is_login:
        return make_response("Unauthorized", 401)

    # creates a dictionary of the form data
    data = request.form

    # returns 400 if necessary data is missing
    if not data:
        return make_response("Data is missing!", 400)

    # gets necessary data
    try:
        stockPrice = json.loads(data.get("stockPrice"))
        optionStrike = json.loads(data.get("optionStrike"))
        optionYears = json.loads(data.get("optionYears"))
        Riskfree = float(data.get("Riskfree"))
        Volatility = float(data.get("Volatility"))

    except:
        return make_response("Necessary data is in an invalid form!")

    # returns 400 if necessary data is missing
    if (
        not stockPrice
        or not optionStrike
        or not optionYears
        or not Riskfree
        or not Volatility
    ):
        return make_response("Finance data is missing!", 400)

    response = Finance.run(
        inputs={
            "stockPrice": stockPrice,
            "optionStrike": optionStrike,
            "optionYears": optionYears,
            "Riskfree": Riskfree,
            "Volatility": Volatility,
        }
    ).get("result")

    callResult = response.get("callResult")
    putResult = response.get("putResult")

    return {
        "callResult": Crypto.run(inputs={"plaintext": callResult}).get("result"),
        "putResult": Crypto.run(inputs={"plaintext": putResult}).get("result"),
    }
