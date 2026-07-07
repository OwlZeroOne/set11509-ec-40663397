from flask import Flask, jsonify, request

import hasher as hsh


app = Flask(__name__)


@app.route("/security/secure", methods=["POST"])
def secure():
    print(request.json)
    password = request.json["password"]
    try:
        hashed = hsh.hash_password(password)
        return jsonify({"result": "success", "hashed": hashed}), 200
    except Exception as e:
        return jsonify({"error": f"in secure(): {str(e)}"}), 400


@app.route("/security/verify", methods=["POST"])
def verify():
    password = request.json["password"]
    hashed = request.json["hashed"]
    try:
        match = hsh.verify_password(hashed, password)
        return jsonify({"result": match}), 200
    except Exception as e:
        return jsonify({"error": f"in verify(): {str(e)}"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)