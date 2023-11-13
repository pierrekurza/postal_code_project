import argparse
import sqlite3

from postal_code_integration import InitDatas


class CityOrPostalCodeSearch:

    def init(self):
        init_data = InitDatas()
        init_data.download_postal_code_file()
        init_data.insert_data_in_db()

    def initiate_db_conn(self) -> sqlite3.Cursor:
        db_conn = sqlite3.connect('postal_codes.db')
        cursor = db_conn.cursor()
        return cursor

    def get_cities_by_postal_code(self, postal_code: str):
        cursor = self.initiate_db_conn()
        sql_query = "select pc.NOM_COMMUNE, pc.AUTRE_VILLE  from POSTAL_CODE pc WHERE pc.CODE_POSTAL LIKE ? "
        cursor.execute(sql_query, postal_code)
        records = cursor.fetchall()
        print(records)

    def get_postal_codes_by_city(self, city: str):
        cursor = self.initiate_db_conn()
        sql_query = "select pc.NOM_COMMUNE, pc.AUTRE_VILLE  from POSTAL_CODE pc WHERE pc.CODE_POSTAL LIKE ? "
        cursor.execute(sql_query, city.upper())
        records = cursor.fetchall()
        print(records)

    def manage_options(self, arguments):
        if arguments.postalcode:
            self.get_cities_by_postal_code(arguments.postalcode)
        elif arguments.city:
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Search City", description="Search cities by postal code")
    parser.add_argument('-c', '--city', metavar='Paris', action='store_true')
    parser.add_argument('-p', '--postalcode', metavar="75000", action='store_true')
    args = parser.parse_args()
    city_or_postal_code_search = CityOrPostalCodeSearch()
    city_or_postal_code_search.manage_options(args)
