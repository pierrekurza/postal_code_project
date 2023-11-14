import sqlite3
import logging
from datetime import datetime
from itertools import chain
from postal_code_integration import InitDatas


class CityOrPostalCodeSearch:

    def __init__(self):
        init_data = InitDatas()
        init_data.download_postal_code_file()
        init_data.insert_data_in_db()

    def initiate_db_conn(self) -> sqlite3.Cursor:
        db_conn = sqlite3.connect('postal_codes.db')
        cursor = db_conn.cursor()
        return cursor

    def get_cities_by_postal_code(self, postal_code: str):
        logging.info("Recherche par code postal avec le numéro {0} à {1}".format(postal_code, datetime.now().strftime("%H:%M:%S")))
        cursor = self.initiate_db_conn()
        sql_query = "select GROUP_CONCAT(NULLIF(pc.NOM_COMMUNE, ' ') || ',' || NULLIF(pc.AUTRE_VILLE, ' ')) FROM POSTAL_CODE pc WHERE pc.CODE_POSTAL LIKE ?"
        cursor.execute(sql_query, [postal_code])
        records = cursor.fetchall()
        print(*list(item for item in list(chain(*records)) if item), sep=',')
        logging.info("Valeurs retournée : {0}".format(*list(item for item in list(chain(*records)) if item), sep=','))
        cursor.close()
        cursor.connection.close()

    def get_postal_codes_by_city(self, city: str):
        logging.info("Recherche par code postal avec le numéro {0} à {1}".format(city, datetime.now().strftime("%H:%M:%S")))
        cursor = self.initiate_db_conn()
        sql_query = "select pc.CODE_POSTAL FROM POSTAL_CODE pc WHERE pc.NOM_COMMUNE LIKE ?"
        cursor.execute(sql_query, [city.upper()])
        records = cursor.fetchall()
        print(*map(lambda x: x[0], records), sep=', ')
        logging.info("Valeurs retournée : {0}".format(*map(lambda x: x[0], records), sep=', '))
        cursor.close()
        cursor.connection.close()

    def manage_options(self, arguments):
        print(arguments)
        if arguments.postalcode:
            self.get_cities_by_postal_code(arguments.postalcode)
        elif arguments.city:
            self.get_postal_codes_by_city(arguments.city)
