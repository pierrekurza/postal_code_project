
import sqlite3

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
        cursor = self.initiate_db_conn()
        sql_query = "select pc.NOM_COMMUNE, pc.AUTRE_VILLE FROM POSTAL_CODE pc WHERE pc.CODE_POSTAL LIKE ? "
        cursor.execute(sql_query, postal_code)
        records = cursor.fetchall()
        print(records)

    def get_postal_codes_by_city(self, city: str):
        cursor = self.initiate_db_conn()
        sql_query = "select pc.NOM_COMMUNE, pc.AUTRE_VILLE FROM POSTAL_CODE pc WHERE pc.CODE_POSTAL LIKE ? "
        cursor.execute(sql_query, city.upper())
        records = cursor.fetchall()
        print(records)

    def manage_options(self, arguments):
        print(arguments)
        if arguments.postalcode:
            self.get_cities_by_postal_code(arguments.postalcode)
        elif arguments.city:
            self.get_postal_codes_by_city(arguments.city)
