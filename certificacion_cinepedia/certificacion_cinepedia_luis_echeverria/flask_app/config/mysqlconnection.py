import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()


def consultar(sql, datos=None):
    """Ejecuta una consulta SQL.
    - SELECT: devuelve una lista de diccionarios
    - INSERT: devuelve el id del registro nuevo
    - UPDATE y DELETE: no devuelven nada útil
    """
    conexion = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, datos)
            if sql.strip().lower().startswith("select"):
                return cursor.fetchall()
            conexion.commit()
            return cursor.lastrowid
    finally:
        conexion.close()