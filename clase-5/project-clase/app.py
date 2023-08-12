from flask import Flask, jsonify, request 
#request -> objeto que contiene la data del cliente
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

#Este es nuestaro MODELO de base de datos: El que representa a una tabla de una base de datos
class User(db.Model): #Heredamos de la clase Model de SQLAlchemy
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(100), unique = False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
        
    def to_json(self):
        return{
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
     

#Configuración de la base de datos MySQL
#Se usa un String, sería el DATABASE_URI,
#Con eso, indicamos que queremos conectar nuestro servidor Flask a la base de datos
#app.config -> es el diccionario que contiene todas las configuraciones del servidor
# Interpretando: mysql+pymysql://root:root@localhost:3306/flask_db
# mysql -> Indica a qué tipo de base de datos vamos a conectarnos. En este caso, una base de datos MySQL
# pymysql -> Indica que usaremos esta dependencia para poder conectarnos
# root:root@localhost:3306/flask_db -> Indicamos el nombre de  (en este caso root), la contraseña, el puerto y, al final, el nombre de la base de datos.
#En resumidas cuentas, con esto le indicamos a Flask cómo conectarse a la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flask_db'

def response(msg, res, cod):
    return jsonify({
        "msg": msg,
        "res": res,
    }), cod

# Definimos los Endpoints
@app.route('/user')
def get_users():
    users: User = User.query.all()
    #Recordar que cuando devolvemos data del backend al frontend, debemos devolverla en formato JSON
    users_json = []
    for user in users:
        users_json.append(user.to_json())
    return response("Usuarios obtenidos", users_json, 200)

@app.route('/user', methods=['POST'])
def add_users():
    try:
        username = request.form['username'] #usamos la forma de pasar datos por formulario
        email = request.form['email']
        # Usaremos el form-data en el body del request (en Postman)
        # También están los query-params -> Son aquellos que aparecen en la URL después del signo ? y se separan por &
        user = User(username, email)
        
        db.session.add(user)
        db.session.commit()
        
        return response("Usuario añadido", user.to_json(), 201) #201: Consulta exitosa y se creo data
    except:
        return response("No se pudo crear el usuario", {}, 500)


@app.route('/user', methods=['PUT'])
def modify_user():
    try:
        #Aquí usamos query-params
        user_id = request.args['user_id']   
        username = request.args['username']   
        email = request.args['email']
        user: User = User.query.get_or_404(user_id)
        user.username =  username
        user.email = email
        db.session.commit()
        return response("Se actualizo el usuario", user.to_json(), 201)
    except:
        return response("No se pudo actualizar el usuario", {}, 500)
     
@app.route('/user', methods=['DELETE'])
def delete_user():
    try:
        user_id = request.args['user_id']
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return response("Usuario borrado", user.to_json(), 200)
    except:
        response("Usuario no pudo ser borrado", {}, 500)

if __name__ == "__main__":
    db.init_app(app) #Con esto, le indicamos al ORM que coopere con nuestro servidor (en este caso, de Flask)
    
    with app.app_context(): #En el contexto de la aplicacion
        db.create_all() #Creamos todas las tablas de la instancia del ORM (que representa a la base de datos)
        
    app.run(debug=True)