import pymysql
import pymysql.cursors

def RemoveTempBan(connector : pymysql.connect, uid):
    cursor = connector.cursor()

    consulta1 = "SELECT * FROM TempBans WHERE UID = %s"
    consulta = "DELETE FROM TempBans WHERE UID = %s"
    VALUES = (uid,)

    cursor.execute(consulta1, VALUES)
    resultados = cursor.fetchall()
    if resultados:
        cursor.execute(consulta, VALUES)
        connector.commit()
        return resultados
    else:
        return False