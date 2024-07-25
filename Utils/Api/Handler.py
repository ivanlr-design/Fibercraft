from flask import Flask, jsonify, request
import pymysql.cursors
import pymysql
import os
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
            if TypeKey == results:
                print(results)

            return jsonify({"Status": "Succesfully auth"}), 200
        else:
            return jsonify({"Status": "Failed To authenticate: INVALID KEY PROVIDED"}), 400
        
    else:
        return jsonify({"Status": "Mysql Error"}), 500


    

def Run():
    db_connection()
    app.run(host='0.0.0.0', port=21902)

    