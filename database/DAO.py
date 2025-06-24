from database.DB_connect import DBConnect
from model.Arco import Arco
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nMin, idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, count(*) as numAirlines
                    from (select a.ID, f.AIRLINE_ID, count(*)
                    from airports a, flights f 
                    where a.ID=f.ORIGIN_AIRPORT_ID or a.ID=f.DESTINATION_AIRPORT_ID
                    group by a.ID, f.AIRLINE_ID) as t
                    group by t.ID
                    having numAirlines>=%s"""

        cursor.execute(query, (nMin,))

        for row in cursor:
            result.append(idMapAirports[row["ID"]])
            # usando idMapAirports tiro fuori un oggetto di tipo Airport dall'ID

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as numVoli
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """
        # la query mi fornisce gli aeroporti di partenza e di arrivo e il numero di voli tra questi due

        cursor.execute(query)

        for row in cursor:
            # metodo1:
            # result.append((idMapAirports[row["ORIGIN_AIRPORT_ID"]], idMapAirports[row["DESTINATION_AIRPORT_ID"]], row["numVoli"]))
            # metodo2: creo un oggetto Arco
            result.append(Arco(idMapAirports[row["ORIGIN_AIRPORT_ID"]], idMapAirports[row["DESTINATION_AIRPORT_ID"]], row["numVoli"]))
        cursor.close()
        conn.close()
        return result