import pymysql
import pymysql.cursors

def SeeIfAuthorized(connector : pymysql.connect, name : str):
    cursor = connector.cursor()

    consulta = f"SELECT * FROM AuthUsers WHERE DiscordName = '{name}'"

    cursor.execute(consulta)
    results = cursor.fetchall()
    if results:
        return results[0]['DiscordID']
    else:
        return False
