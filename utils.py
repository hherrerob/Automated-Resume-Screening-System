from flask import jsonify


def make_response(status, message):
    raw_response = {
        "status": status
    }

    if status == 200:
        raw_response["results"] = message
    else:
        raw_response["message"] = message

    resp = jsonify(raw_response)
    resp.status_code = status

    return resp
