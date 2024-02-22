import pymysql
import pymysql.cursors

def SeeIfAuthorized(connector : pymysql.connect, name : str):
    cursor = connector.cursor()

    consulta = "SELECT * FROM AuthUsers WHERE DiscordName = %s"
    VALUES = (name, )
    cursor.execute(consulta, VALUES)
    results = cursor.fetchall()
    if results:
        return results[0]['DiscordID']
    else:
        return False
