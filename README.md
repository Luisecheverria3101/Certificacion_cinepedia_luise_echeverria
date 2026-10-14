# CinePedia — Certificación FullStack Python Skillnest

**Examen de Certificación FullStack Python, Skillnest 2026**

## Datos del estudiante

- **Nombre:** Luis Echeverría
- **Curso:** 4°C
- **Fecha:** 14/10/2026

## Descripción y tecnologías

CinePedia es una aplicación web para la gestión y consulta de películas, desarrollada con Python y Flask siguiendo una estructura basada en el patrón arquitectónico **MVC (Modelo-Vista-Controlador)**.

El proyecto organiza sus funcionalidades mediante controladores, modelos, plantillas HTML y archivos de configuración. Utiliza **MySQL** para almacenar los datos, **PyMySQL** para establecer la conexión con la base de datos y **HTML y CSS** para construir la interfaz de usuario.

La aplicación incluye módulos para gestionar películas, usuarios y comentarios, además de páginas para visualizar información, registrar datos y navegar por las distintas funcionalidades del sistema.

## Estructura de carpetas

```text
CinePedia_Certificacion_FullStack-Python_Skillnest/
│
├── certificacion_cinepedia/
│   │
│   ├── flask_app/
│   │   │
│   │   ├── config/
│   │   │   ├── __pycache__/
│   │   │   ├── __init__.py
│   │   │   └── pymysqlconnection.py
│   │   │
│   │   ├── controllers/
│   │   │   ├── __pycache__/
│   │   │   ├── peliculas.py
│   │   │   └── usuarios.py
│   │   │
│   │   ├── models/
│   │   │   ├── __pycache__/
│   │   │   ├── comentario.py
│   │   │   ├── pelicula.py
│   │   │   └── usuario.py
│   │   │
│   │   ├── resources/
│   │   │   └── DB/
│   │   │       ├── cinepedia.sql
│   │   │       └── ERD.png
│   │   │
│   │   ├── static/
│   │   │   └── css/
│   │   │       └── style.css
│   │   │
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── dashboard.html
│   │   │   ├── formulario.html
│   │   │   ├── index.html
│   │   │   └── ver.html
│   │   │
│   │   ├── .env
│   │   └── app.py
│   │
│   ├── .gitignore
│   ├── Pipfile
│   ├── requirements.txt
│   └── server.py
│
└── README.md
```

