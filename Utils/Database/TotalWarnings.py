import pymysql
import pymysql.cursors

def TotalWarnings(connector : pymysql.connect, tribename : str):
    cursor = connector.cursor()

    consulta = f"SELECT * FROM Punishments WHERE TribeName = '{tribename}'"

    cursor.execute(consulta)
    results = cursor.fetchall()
    if results:
        seasonals = 0
        permanent = 0
        verbal = 0
        for result in results:
            if result['Warning_type'] == "Seasonal Warning":
                seasonals += result['Warnings']
            elif result['Warning_type'] == "Permanent Warning":
                permanent += result['Warnings']
            elif result['Warning_type'] == "Verbal Warning":
                verbal += result['Warnings']
        
        return seasonals,permanent,verbal
    else:
        return False