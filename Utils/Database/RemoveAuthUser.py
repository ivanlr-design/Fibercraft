import pymysql
import pymysql.cursors

def RemoveAuthUser(connector : pymysql.connect, username):
    cursor = connector.cursor()

    consulta1 = "SELECT * FROM AuthUsers WHERE DiscordName = %s"
    consulta = "DELETE FROM AuthUsers WHERE DiscordName = %s"
    VALUES = (username, )
    cursor.execute(consulta1, VALUES)
    result = cursor.fetchall()
    if result:
        cursor.execute(consulta, VALUES)
        connector.commit()
        return result
    else:
        return False
    