from flask import render_template, request, redirect, session
from flask_app.app import app
from flask_app.models.usuario import crear_usuario, validar_registro, validar_login


@app.route("/")
def inicio():
    # Si ya inició sesión, lo mandamos al dashboard
    if "usuario_id" in session:
        return redirect("/cine")
    return render_template("index.html")


@app.route("/registro", methods=["POST"])
def registro():
    nombre = request.form["nombre"].strip()
    apellido = request.form["apellido"].strip()
    email = request.form["email"].strip().lower()
    password = request.form["password"]
    confirmar = request.form["confirmar"]

    errores = validar_registro(nombre, apellido, email, password, confirmar)
    if errores:
        # Volvemos al formulario, conservando lo que escribió
        return render_template(
            "index.html", errores_registro=errores,
            nombre=nombre, apellido=apellido, email=email,
        )

    usuario_id = crear_usuario(nombre, apellido, email, password)
    session["usuario_id"] = usuario_id
    session["nombre"] = nombre
    return redirect("/cine")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email_login"].strip().lower()
    password = request.form["password_login"]

    usuario = validar_login(email, password)
    if usuario is None:
        return render_template(
            "index.html", errores_login=["Email o contraseña incorrectos."], email_login=email
        )

    session["usuario_id"] = usuario["id"]
    session["nombre"] = usuario["nombre"]
    return redirect("/cine")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")