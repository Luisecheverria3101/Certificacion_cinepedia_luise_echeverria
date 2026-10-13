from flask_app.config.mysqlconnection import consultar


def comentarios_de_pelicula(pelicula_id):
    # Los más recientes primero
    return consultar(
        "SELECT comentarios.*, usuarios.nombre "
        "FROM comentarios JOIN usuarios ON usuarios.id = comentarios.usuario_id "
        "WHERE pelicula_id = %s ORDER BY comentarios.id DESC",
        (pelicula_id,),
    )


def buscar_comentario(id):
    resultado = consultar("SELECT * FROM comentarios WHERE id = %s", (id,))
    if resultado:
        return resultado[0]
    return None


def crear_comentario(contenido, usuario_id, pelicula_id):
    return consultar(
        "INSERT INTO comentarios (contenido, usuario_id, pelicula_id) VALUES (%s, %s, %s)",
        (contenido, usuario_id, pelicula_id),
    )


def borrar_comentario(id):
    return consultar("DELETE FROM comentarios WHERE id = %s", (id,))