import pymysql
import pymysql.cursors

def AddTempBan(connection : pymysql.connect, Names, SteamIDs, TribeName, Reason, UnbanDate, UID, Author, Made):
    cursor = connection.cursor()

    consulta = "INSERT INTO TempBans (TribeName, Names, SteamIDs, Reason, UnbanDate, UID, Author, Made) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    VALUES = (TribeName, Names, SteamIDs, Reason, UnbanDate, UID, Author, Made)

    cursor.execute(consulta,VALUES)
    try:
        connection.commit()
        return True
    except:
        return False

