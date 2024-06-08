from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/v1/CheckKey", methods=["POST"])
def CheckKey():

    if not request.is_json:
        return jsonify({"Error":"Contenido debe ser JSON"}), 400

    data = request.get_json()

    APIKey = data.get("APIKey")
    Key = data.get("Key")
    TypeKey = data.get("TypeKey")
    HWID = data.get("HWID")

    print (APIKey + " " + Key + " " + TypeKey + " " + HWID)
    return jsonify({"Authenticated": "Succesfully auth"}), 200

def Run():
    app.run(host='0.0.0.0', port=80)

    