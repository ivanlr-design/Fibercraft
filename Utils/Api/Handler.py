from flask import Flask, jsonify, request
import pymysql.cursors
import pymysql
import os
import hashlib
from dotenv import load_dotenv, dotenv_values
load_dotenv(".env")

MYSQL_CONNECT = os.getenv("MYSQL_CONNECTOR")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWD = os.getenv("MYSQL_PASSWD")

app = Flask(__name__)

def db_connection():
    print(MYSQL_CONNECT)
    connection = pymysql.connect(host=MYSQL_CONNECT,
                                user=MYSQL_USER,
                                password=MYSQL_PASSWD,
                                db='s51219_punish',
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)

    return connection

@app.route("/api/v1/CheckKey", methods=["GET"])
def CheckKey():

    apikey = request.args.get("ApiKey")
    Key = request.args.get("Key")
    HWID = request.args.get("HWID")
    TypeKey = request.args.get("TypeKey")
    
    md5_hash = hashlib.md5(apikey.encode()).hexdigest()

    if md5_hash != "9828858d6c3b1658791eaa25989538bb":
        return jsonify({"Status": "Not Authenticated, err code: 0x20"}), 400

    if not apikey or not Key or not HWID or not TypeKey:
        return jsonify({"Status": "Corrupted"}), 400

    conection = db_connection()
    if conection:
        cursor = conection.cursor()
        consulta = "SELECT Type FROM KeysValidation WHERE ValidKey = %s"
        VALUES = (Key, )
        cursor.execute(consulta, VALUES)
        results = cursor.fetchall()
        if results:
            for result in results:
                print(result)
                if TypeKey == result or result == "Pruebas":
                    consulta = "SELECT HWID FROM KeysValidation WHERE ValidKey = %s"
                    VALUES = (Key, )
                    cursor.execute(consulta, VALUES)
                    results = cursor.fetchall()
                    for result in results:
                        if result == HWID:
                            return jsonify({"Status": "Succesfully auth"}), 200
                        else:
                            return jsonify({"Status": "Failed to Auth: Err code 0x26"}), 400 
                else:
                    return jsonify({"Status": "Failed to Auth: Err code 0x25"}), 400

                
        else:
            return jsonify({"Status": "Failed To authenticate: Err code 0x24"}), 400
        
    else:
        return jsonify({"Status": "Mysql Error"}), 500


    

def Run():
    db_connection()
    app.run(host='0.0.0.0', port=21902)

    