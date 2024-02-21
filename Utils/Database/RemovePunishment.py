import pymysql
import pymysql.cursors

def RemovePunishment(connect : pymysql.connect, uid):
    cursor = connect.cursor()

    consulta = f"DELETE FROM Punishments WHERE UID = '{uid}'"
    consulta2 = f"SELECT * FROM Punishments WHERE UID = '{uid}'"

    cursor.execute(consulta2)
    results = cursor.fetchall()
    if results:
        cursor.execute(consulta)
        connect.commit()
    else:
        return False
