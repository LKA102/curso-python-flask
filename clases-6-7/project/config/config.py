from flask import Flask
from flask_jwt_extended import JWTManager #Clase que representa al manager de los JWTs a utilizar
from flask_bcrypt import Bcrypt #Clase que representa al sistema de encriptación a utilizar

def config_app(name):
    app = Flask(name)
    # configuramos el string de conexión con el servidor de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flask_db'
    app.secret_key = 'SECRET_KEY' #Seteamos una clave secreta. Usualmente esta debe estar en un archivo .env de variables de entorno
    #NO SE DEBE PUBLICAR LA CLAVE SECRETA, sino cualquiera puede desencriptar las contraseñas. 
    #La clave secreta se utiliza en el algoritmo de encriptación
    #Solo nosotros debemos saberla.
    return app

bcrypt = Bcrypt()
jwt = JWTManager()