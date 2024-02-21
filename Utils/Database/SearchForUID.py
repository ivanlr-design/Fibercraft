import pymysql
import pymysql.cursors

def SearchForUid(connect : pymysql.connect, UID):
    cursor = connect.cursor()

    consulta = f"SELECT * FROM Punishments WHERE UID = '{UID}' "

    cursor.execute(consulta)
    resultados = cursor.fetchall()

    if resultados:
        return resultados
    else:
        return False