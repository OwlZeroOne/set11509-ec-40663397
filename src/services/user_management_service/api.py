import db

from flask import Flask, request, jsonify

app = Flask(__name__)
repo = db.Repository()


@app.route("/user-mngmt-service/get-all-users", methods=["GET"])
def get_all_users():
    users = repo.get_all_users()
    try:
        return jsonify({"result": "success", "users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/user-mngmt-service/new-user", methods=["POST"])
def new_user():
    try:
        args = request.json
    except Exception as e:
        return jsonify({"error": "bad request"}), 400

    try:
        repo.add_user(**args)
        return jsonify({"result": "success"}), 201
    except Exception as e:
        return jsonify({"error": "internal error"}), 500


@app.route("/user-mngmt-service/update-user", methods=["PUT"])
def update_user():
    uid = request.json["uid"]
    user = repo.get_user_by_id(uid)
    if user is not None:
        args = request.json['attributes']
        repo.update_user(uid, **args)
        return jsonify({"result": "success"}), 200
    else:
        return jsonify({"error": "user not found"}), 404


@app.route("/user-mngmt-service/delete-user", methods=["DELETE"])
def delete_user():
    uid = request.json["uid"]
    user = repo.get_user_by_id(uid)
    if user is not None:
        repo.delete_user(uid)
        return jsonify({"result": "success"}), 200
    else:
        return jsonify({"error": "user not found"}), 404


@app.route("/user-mngmt-service/get-user", methods=["POST"])
def get_user():
    try:
        username = request.json["username"]
    except Exception as e:
        return jsonify({
            "error": "bad request",
            "params": request.json,
            "body": str(e)
        }), 400

    try:
        user = repo.get_user_by_username(username)
    except Exception as e:
        return jsonify({
            "error": "internal error",
            "body": str(e)
        }), 500

    if user is not None:
        return jsonify({"result": "success", "user": user.to_dict()}), 200
    else:
        return jsonify({"error": "user not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
