import pymysql
import pymysql.cursors

def AddPunishment(connection : pymysql.connect, Names, SteamIDs, Reason, TribeName, Punishment, Warning_type, Warnings, UID):
    consulta = 'INSERT INTO Punishments (Names, SteamIDS, Reason, TribeName, Punishment, Warning_type, Warnings, UID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    VALUES = (Names, SteamIDs, Reason, TribeName, Punishment, Warning_type, Warnings, UID)

    cursor = connection.cursor()
    cursor.execute(consulta, VALUES)

    try:
        connection.commit()
        return True
    except Exception as e:
        return False