import pymysql
import pymysql.cursors

def AddAuthUser(connector : pymysql.connect, username : str, id : int):
    cursor = connector.cursor()
    consulta2 = f"SELECT * FROM AuthUsers WHERE DiscordID = {id}"
    consulta = "INSERT INTO AuthUsers (DiscordID, DiscordName) VALUES (%s,%s)"
    VALUES = (id, username)

    cursor.execute(consulta2)
    resultados = cursor.fetchall()
    if resultados:
        return resultados[0]['DiscordID']
    else:
        cursor.execute(consulta, VALUES)
        connector.commit()
        return True
