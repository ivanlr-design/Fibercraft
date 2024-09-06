import pymysql
import pymysql.cursors

async def ClearPendingConections(connector : pymysql.connect):
    cursor = connector.cursor()

    consulta = "SELECT CONCAT('KILL ', id, ';') AS kill_query FROM information_schema.processlist WHERE command = 'Sleep' AND time > 1;"
    cursor.execute(consulta)
    results = cursor.fetchall()

    if results:
        index = 0
        for result in results:
            killQuery = results[index]['kill_query']
            try:
            
                cursor.execute(killQuery)
            except Exception as e:
                print("[!] - Error: " + str(e))