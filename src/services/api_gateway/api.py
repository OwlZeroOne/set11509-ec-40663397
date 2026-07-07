import requests

from flask import Flask, request, jsonify

app = Flask(__name__)

UMS_URL = "http://user-mngmt-service:5000"
PASSWORD_URL = "http://password-service:5001"
AUTH_URL = "http://authentication-service:5002"
SHARE_URL = "http://share-data-service:5003"
BROKERS_URL = "http://broker-service:5004"

DEBUG = True


def forward(url, method, body=None):
    headers = {}
    if body:
        headers["Content-Type"] = "application/json"

    response = requests.request(
        method=method,
        url=url,
        json=body,
        headers=headers
    )
    try:
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": "empty ot invalid response"}), response.status_code


def validate_token():
    if DEBUG:
        return True
    token = request.headers.get("Authorization")
    response = requests.post(
        f"{AUTH_URL}/auth/validate",
        headers={"Authorization": token},
    )
    return response.status_code == 200


@app.route("/gateway/login", methods=["POST"])
def login():
    return forward(
        f"{AUTH_URL}/auth/login",
        "POST",
        request.get_json(force=True, silent=True)
    )


@app.route("/gateway/register", methods=["POST"])
def register():
    return forward(
        f"{UMS_URL}/user-mngmt-service/new-user",
        "POST",
        request.get_json(force=True, silent=True)
    )


# UMS Routes
@app.route("/gateway/users/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def users(path):
    if not validate_token():
        return jsonify({"error": "unauthorised"}), 401

    return forward(
        f"{UMS_URL}/user-mngmt-service/{path}",
        request.method,
        request.get_json(force=True, silent=True)
    )


# Password Routes
@app.route("/gateway/security/<path:path>", methods=["POST"])
def security(path):
    return forward(
        f"{PASSWORD_URL}/security/{path}",
        request.method,
        request.get_json(force=True, silent=True)
    )


@app.route("/gateway/shares/<path:path>", methods=["GET", "POST"])
def shares(path):
    if not validate_token():
        return jsonify({"error": "unauthorised"}), 401
    return forward(
        f"{SHARE_URL}/shares/{path}",
        request.method,
        request.get_json(force=True, silent=True)
    )



@app.route("/gateway/brokers/<path:path>", methods=["GET"])
def brokers(path):
    if not validate_token():
        return jsonify({"error": "unauthorised"}), 401
    return forward(
        f"{BROKERS_URL}/broker-service/{path}",
        request.method,
        request.get_json(force=True, silent=True)
    )


# @app.route("/gateway/history/<path:path>", methods=["POST"])
# def history(path):
#     if not validate_token():
#         return jsonify({"error": "unauthorised"}), 401
#     return forward(
#         f"{SHARE_URL}/history/{path}",
#         request.method,
#         request.get_json(force=True, silent=True)
#     )


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5010,debug=True)

