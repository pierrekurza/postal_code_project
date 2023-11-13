import requests
import pandas as panda
import sqlite3
import os


class InitDatas:
    def __init__(self):
        pass

    def download_postal_code_file(self):
        url = "https://datanova.laposte.fr/data-fair/api/v1/datasets/laposte-hexasmal/raw"
        req = requests.get(url, allow_redirects=True)
        open('postal_codes.csv', 'wb').write(req.content)

    def insert_data_in_db(self):
        if os.path.exists("postal_codes.db"):
            os.remove("postal_codes.db")
        else:
            print("postal_codes.db n'\\est pas présent")
        db_connection = sqlite3.connect("postal_codes.db")
        db_connection.set_trace_callback(print)
        cursor = db_connection.cursor()
        create_table = '''CREATE TABLE IF NOT EXISTS POSTAL_CODE (NOM_COMMUNE, CODE_POSTAL, AUTRE_VILLE)'''
        cursor.execute(create_table)

        df = panda.read_csv('postal_codes.csv', encoding='latin-1', sep=";", keep_default_na=False)
        for index, row in df.iterrows():
            insert_query = f"""
                INSERT INTO POSTAL_CODE (NOM_COMMUNE, CODE_POSTAL, AUTRE_VILLE)
                VALUES ( "{row['Nom_de_la_commune']}", "{row['Code_postal']}", "{(row['Ligne_5'], "")[row['Ligne_5'] == '']}");
            """
            cursor.execute(insert_query)
        db_connection.commit()
        cursor.close()
        db_connection.close()

