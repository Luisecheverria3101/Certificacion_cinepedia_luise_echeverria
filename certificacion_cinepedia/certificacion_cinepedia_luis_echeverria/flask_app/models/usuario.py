import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app.config.mysqlconnection import consultar

# Formato básico de un email: algo@algo.algo
FORMATO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]+$")


def buscar_por_email(email):
    resultado = consultar("SELECT * FROM usuarios WHERE email = %s", (email,))
    if resultado:
        return resultado[0]
    return None


def crear_usuario(nombre, apellido, email, password):
    # La contraseña se guarda cifrada, nunca en texto normal
    clave_cifrada = generate_password_hash(password)
    return consultar(
        "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)",
        (nombre, apellido, email, clave_cifrada),
    )


def validar_registro(nombre, apellido, email, password, confirmar):
    errores = []
    if len(nombre) < 2:
        errores.append("El nombre debe tener al menos 2 caracteres.")
    if len(apellido) < 2:
        errores.append("El apellido debe tener al menos 2 caracteres.")
    if not FORMATO_EMAIL.match(email):
        errores.append("El email no tiene un formato válido.")
    elif buscar_por_email(email):
        errores.append("Ese email ya está registrado.")
    if len(password) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres.")
    if password != confirmar:
        errores.append("La contraseña y su confirmación deben ser iguales.")
    return errores


def validar_login(email, password):
    """Devuelve el usuario si los datos son correctos, si no devuelve None."""
    usuario = buscar_por_email(email)
    if usuario and check_password_hash(usuario["password"], password):
        return usuario
    return None