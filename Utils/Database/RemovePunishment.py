import pymysql
import pymysql.cursors

def RemovePunishment(connect : pymysql.connect, uid):
    cursor = connect.cursor()

    consulta = "DELETE FROM Punishments WHERE UID = %s"
    consulta2 = "SELECT * FROM Punishments WHERE UID = %s"
    VALUES = (uid, )
    cursor.execute(consulta2, VALUES)
    results = cursor.fetchall()
    if results:
        cursor.execute(consulta, VALUES)
        connect.commit()
    else:
        return False
