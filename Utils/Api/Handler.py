from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/v1/CheckKey", methods=["GET"])
def CheckKey():

    apikey = request.args.get("ApiKey")
    Key = request.args.get("Key")
    HWID = request.args.get("HWID")
    TypeKey = request.args.get("TypeKey")
    print(apikey)
    print(Key)
    print(HWID)
    print(TypeKey)
    if not apikey or not Key or not HWID or not TypeKey:
        return jsonify({"Failed to Authenticate": "Not enough arguments"}), 400

    return jsonify({"Authenticated": "Succesfully auth"}), 200

def Run():
    app.run(host='0.0.0.0', port=21902)

    