import pymysql
import pymysql.cursors

def SearchForID(connect : pymysql.connect, ID : str):
    cursor = connect.cursor()
    consulta = "SELECT * FROM Punishments WHERE SteamIDS LIKE '%{}%'".format(ID)

    cursor.execute(consulta)
    resultados = cursor.fetchall()
    if resultados:
        return resultados
    else:
        return False