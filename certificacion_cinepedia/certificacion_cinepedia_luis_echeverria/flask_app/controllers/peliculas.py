from flask import render_template, request, redirect, session, flash
from flask_app.app import app
from flask_app.models.pelicula import (
    obtener_todas, obtener_una, crear_pelicula,
    actualizar_pelicula, borrar_pelicula, validar_pelicula,
)
from flask_app.models.comentario import (
    comentarios_de_pelicula, buscar_comentario, crear_comentario, borrar_comentario,
)


def datos_del_formulario():
    """Saca los datos de la película desde el formulario"""
    return {
        "titulo": request.form["titulo"].strip(),
        "director": request.form["director"].strip(),
        "fecha_estreno": request.form["fecha_estreno"],
        "sinopsis": request.form["sinopsis"].strip(),
    }


@app.route("/cine")
def dashboard():
    if "usuario_id" not in session:
        return redirect("/")
    return render_template("dashboard.html", peliculas=obtener_todas())


@app.route("/cine/nueva", methods=["GET", "POST"])
def nueva():
    if "usuario_id" not in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("formulario.html", titulo_pagina="Nueva Película", datos={}, errores=[])

    datos = datos_del_formulario()
    errores = validar_pelicula(datos)
    if errores:
        return render_template("formulario.html", titulo_pagina="Nueva Película", datos=datos, errores=errores)

    datos["usuario_id"] = session["usuario_id"]
    crear_pelicula(datos)
    return redirect("/cine")


@app.route("/cine/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if "usuario_id" not in session:
        return redirect("/")

    pelicula = obtener_una(id)
    # Solo puede editar quien la creó
    if pelicula is None or pelicula["usuario_id"] != session["usuario_id"]:
        return redirect("/cine")

    if request.method == "GET":
        # Mostramos el formulario con los datos de la pelicula
        return render_template("formulario.html", titulo_pagina="Editar Película", datos=pelicula, errores=[])

    datos = datos_del_formulario()
    errores = validar_pelicula(datos, id)
    if errores:
        return render_template("formulario.html", titulo_pagina="Editar Película", datos=datos, errores=errores)

    actualizar_pelicula(id, datos)
    return redirect("/cine")


@app.route("/cine/borrar/<int:id>", methods=["POST"])
def borrar(id):
    if "usuario_id" not in session:
        return redirect("/")

    pelicula = obtener_una(id)
    # Solo puede borrar quien la creó
    if pelicula is not None and pelicula["usuario_id"] == session["usuario_id"]:
        borrar_pelicula(id)
    return redirect("/cine")


@app.route("/cine/<int:id>")
def ver(id):
    if "usuario_id" not in session:
        return redirect("/")

    pelicula = obtener_una(id)
    if pelicula is None:
        return redirect("/cine")

    comentarios = comentarios_de_pelicula(id)
    # No se puede comentar la propia película
    puede_comentar = pelicula["usuario_id"] != session["usuario_id"]
    return render_template("ver.html", pelicula=pelicula, comentarios=comentarios, puede_comentar=puede_comentar)


@app.route("/cine/<int:id>/comentar", methods=["POST"])
def comentar(id):
    if "usuario_id" not in session:
        return redirect("/")

    pelicula = obtener_una(id)
    if pelicula is None or pelicula["usuario_id"] == session["usuario_id"]:
        return redirect("/cine")

    contenido = request.form["contenido"].strip()
    if contenido == "":
        flash("El comentario no puede estar vacío.")
    else:
        crear_comentario(contenido, session["usuario_id"], id)
    return redirect("/cine/" + str(id))


@app.route("/cine/comentario/borrar/<int:id>", methods=["POST"])
def borrar_un_comentario(id):
    if "usuario_id" not in session:
        return redirect("/")

    comentario = buscar_comentario(id)
    if comentario is None:
        return redirect("/cine")

    # Solo puede borrar sus propios comentarios
    if comentario["usuario_id"] == session["usuario_id"]:
        borrar_comentario(id)
    return redirect("/cine/" + str(comentario["pelicula_id"]))