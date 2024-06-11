from database.DB_connect import DBConnect
from model.Retailer import Retailer
from model.Connessione import Connessione


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct(gr.Country)
                    from go_retailers gr  """

        cursor.execute(query)

        for row in cursor:
            result.append(row['Country'])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getNodi(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
            from go_retailers gr 
            where gr.Country =%s"""

        cursor.execute(query,(country,))

        for row in cursor:
            result.append(Retailer(row['Retailer_code'],row['Retailer_name']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def GetConnessioni(year,country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT gds1.Retailer_code as r1 , gds2.Retailer_code as r2,gds2.Product_number as pn
                from go_daily_sales gds2
                join go_daily_sales gds1 on gds1.Product_number = gds2.Product_number
                JOIN go_retailers gr1  on gds1.Retailer_code  = gr1.Retailer_code 
                JOIN go_retailers gr2  on gr2.Retailer_code  = gds2.Retailer_code
                where gds1.Retailer_code <gds2.Retailer_code and YEAR (gds1.Date)=%s and YEAR (gds2.Date)=YEAR (gds1.Date) and gr2.Country = %s
                and gr1.Country= gr2.Country
                group by gds1.Retailer_code , gds2.Retailer_code,gds2.Product_number"""

        cursor.execute(query, (year,country))

        for row in cursor:
            result.append(Connessione(row['r1'],row['r2'],row['pn']))

        cursor.close()
        conn.close()
        return result