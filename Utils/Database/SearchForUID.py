import pymysql
import pymysql.cursors

def SearchForUid(connect : pymysql.connect, UID):
    cursor = connect.cursor()

    consulta = "SELECT * FROM Punishments WHERE UID = %s "
    
    cursor.execute(consulta, (UID,))
    resultados = cursor.fetchall()

    if resultados:
        return resultados
    else:
        return False