import pymysql
import pymysql.cursors

def searchforTribename(connector : pymysql.connect, tribename):
    cursor = connector.cursor()

    consulta = "SELECT * FROM Punishments WHERE TribeName = %s"
    VALUES = (tribename, )
    cursor.execute(consulta, VALUES)
    resultados = cursor.fetchall()

    if resultados:
        return resultados
    else:
        return False