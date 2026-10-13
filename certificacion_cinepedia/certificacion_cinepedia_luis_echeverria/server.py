from flask_app.app import app

# Al importar los controladores se registran las rutas
from flask_app.controllers import usuarios, peliculas

if __name__ == "__main__":
    app.run(debug=True, port=5000)