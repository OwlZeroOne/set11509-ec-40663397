import jwt
import datetime
import requests

from flask import jsonify, request, Flask

app = Flask(__name__)

SECRET_KEY = "Super secret key"
UMS_URL = "http://user-mngmt-service:5000"
PASSWORD_URL = "http://password-service:5001"

def generate_token(user: dict) -> str:
    payload = {
        "uid": user["uid"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


@app.route("/auth/login", methods=["POST"])
def login():
    body = request.get_json(force=True, silent=True)
    ums_response = requests.post(
        f"{UMS_URL}/user-mngmt-service/get-user",
        json=body
    )
    ums_response_body = ums_response.json()
    if "user" not in ums_response_body:
        return jsonify({"result": "bad request", "body": ums_response_body}), 400
    else:
        user = ums_response_body["user"]

    verify_response = requests.post(
        f"{PASSWORD_URL}/security/verify",
        json={"password": body["password"], "hashed": user["password_hash"]}
    )
    if not verify_response.json().get("result"):
        return jsonify({"result": "unauthorised"}), 401

    token = generate_token(user)
    return jsonify({"result": "success", "token": token, "user": user}), 200


@app.route("/auth/validate", methods =["POST"])
def validate():
    auth = request.headers.get("Authorization")
    if not auth:
        return jsonify({"result": "token missing"}), 401

    parts = auth.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({"error": "invalid token format"}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({
            "result": "success",
            "payload": payload}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002 ,debug=True)