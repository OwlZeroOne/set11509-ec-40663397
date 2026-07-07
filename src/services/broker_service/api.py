import db

from flask import Flask, jsonify, request

app = Flask(__name__)
repo = db.Repository()


@app.route("/broker-service/get-all", methods=['GET'])
def get_all_brokers():
    brokers = repo.get_all()
    try:
        return jsonify({"result": "success", "brokers": brokers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/broker-service/get-by-domains", methods=['GET'])
def get_broker_by_domain():
    body = request.get_json(force=True, silent=True)
    domains = body.get("domains")
    try:
        brokers = repo.get_by_domains(domains)
        return jsonify({"result": "success", "brokers": brokers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/broker-service/get-all-except", methods=['GET'])
def get_all_brokers_except():
    body = request.get_json(force=True, silent=True)
    domains = body.get("domains")
    try:
        brokers = repo.get_all_except(domains)
        return jsonify({"result": "success", "brokers": brokers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)