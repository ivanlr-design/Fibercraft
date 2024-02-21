import pymysql
import pymysql.cursors

def searchforTribename(connector : pymysql.connect, tribename):
    cursor = connector.cursor()

    consulta = f"SELECT * FROM Punishments WHERE TribeName = '{tribename}'"

    cursor.execute(consulta)
    resultados = cursor.fetchall()

    if resultados:
        return resultados
    else:
        return False