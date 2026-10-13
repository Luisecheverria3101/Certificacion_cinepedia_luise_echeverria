from datetime import datetime
from flask_app.config.mysqlconnection import consultar


def obtener_todas():
    return consultar("SELECT * FROM peliculas ORDER BY id DESC")


def obtener_una(id):
    # Con JOIN traemos también el nombre de quien la publicó
    resultado = consultar(
        "SELECT peliculas.*, usuarios.nombre AS publicador "
        "FROM peliculas JOIN usuarios ON usuarios.id = peliculas.usuario_id "
        "WHERE peliculas.id = %s",
        (id,),
    )
    if resultado:
        return resultado[0]
    return None


def crear_pelicula(datos):
    # datos es un diccionario con titulo, director, fecha_estreno, sinopsis y usuario_id
    return consultar(
        "INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id) "
        "VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s)",
        datos,
    )


def actualizar_pelicula(id, datos):
    datos["id"] = id
    return consultar(
        "UPDATE peliculas SET titulo=%(titulo)s, director=%(director)s, "
        "fecha_estreno=%(fecha_estreno)s, sinopsis=%(sinopsis)s WHERE id=%(id)s",
        datos,
    )


def borrar_pelicula(id):
    return consultar("DELETE FROM peliculas WHERE id = %s", (id,))


def validar_pelicula(datos, id_actual=0):
    """id_actual sirve al editar: así puede dejar su mismo nombre."""
    errores = []

    if len(datos["titulo"]) < 3:
        errores.append("El nombre de la película debe tener al menos 3 caracteres.")
    else:
        # Bonus: el nombre no se puede repetir
        repetida = consultar(
            "SELECT id FROM peliculas WHERE titulo = %s AND id != %s",
            (datos["titulo"], id_actual),
        )
        if repetida:
            errores.append("Ya existe una película con ese nombre.")

    if len(datos["director"]) < 3:
        errores.append("El director debe tener al menos 3 caracteres.")

    if datos["fecha_estreno"] == "":
        errores.append("Fecha de estreno no puede estar vacía.")
    else:
        try:
            datetime.strptime(datos["fecha_estreno"], "%Y-%m-%d")
        except ValueError:
            errores.append("La fecha de estreno no es válida.")

    if datos["sinopsis"] == "":
        errores.append("Sinopsis no puede estar vacía.")
    elif len(datos["sinopsis"]) < 3:
        errores.append("La sinopsis debe tener al menos 3 caracteres.")

    return errores