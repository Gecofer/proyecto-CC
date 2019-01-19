# ---------------------------------- main.py --------------------------------- #

# Autora: Gema Correa Fernández

'''
Fichero que implementa la clase API REST haciendo uso del microframework Flask
'''

# Bibliotecas a usar
from flask import Flask     # importamos la clase Flask
from flask import jsonify   # https://pypi.org/project/Flask-Jsonpify/
from flask import request   # https://github.com/requests/requests

from flask import render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

import json
import os
from data import *

# Para la creación del log
import logging
logger = logging.getLogger("app")
logging.basicConfig(filename = "debug.log", filemode = 'a', format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.DEBUG)

# Creación de una instancia de la clase Flask
app = Flask(__name__)

logger.info("Successfully run Flask application.")

# ---------------------------------------------------------------------------- #

# Mysql Connection
app.config['MYSQL_HOST'] = '10.0.0.5'
app.config['MYSQL_USER'] = 'usuariocc'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'twitter'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# ---------------------------------------------------------------------------- #

# routes
@app.route('/BD')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data, content_type='application/json')

# ---------------------------------------------------------------------------- #

@app.route('/add_bd', methods=['POST'])
def add_bd():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        tweet_volume = request.form['tweet_volume']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (name, url, tweet_volume) VALUES ( %s,%s,%s)", (name, url, tweet_volume))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

# ---------------------------------------------------------------------------- #

# Obtenemos los datos
try:
    with open('data/data.json', encoding='utf-8') as data_file:
        data_twitter = json.loads(data_file.read())
        logger.info("Successfully read file JSON.")
except IOError as fail:
    logger.error("Unsuccessfully read file JSON.")
    print("Error %d reading %s", fail.errno, fail.strerror)

# ---------------------------------------------------------------------------- #

# Ruta para comprobar que se ha desplegado de forma correcta
@app.route('/')
@app.route('/status')
def index():

    # Añadimos mensaje para comprobar que se ha desplegado de forma correcta
    logger.info("Successfully status application in '/' or '/status' - Status 200")

    return jsonify(status='OK') # devolvemos { "status": "OK" }

# ---------------------------------------------------------------------------- #

# Mostrar un 404, cuando se ha desplegado de forma incorrecta
# Código de estado HTTP: https://developer.mozilla.org/es/docs/Web/HTTP/Status
@app.errorhandler(404)
def not_found(error):

    data = {} # definimos un diccionario
    data['msg error'] = 'URL not found'

    # jsonify: convierte la salida JSON en un objeto Response con
    # la aplication/json mimetype
    result = jsonify(data)

    # Se modifica el código de estado de la respuesta a 404
    # 404: Recurso no encontrado, el servidor web no encuentra la página
    # http://docs.python-requests.org/en/master/user/quickstart/
    result.status_code = 404

    # Añadimos mensaje para comprobar que se ha desplegado de forma incorrecta
    logger.error("404 Not Found: The requested URL was not found on the server - Status 404")

    return result # devolvemos { "msg error": "URL not found" }

# ---------------------------------------------------------------------------- #

# Mostrar un 405, cuando el método es no permitido
# Código de estado HTTP: https://developer.mozilla.org/es/docs/Web/HTTP/Status
@app.errorhandler(405)

def not_found(error):
    data = {} # definimos un diccionario
    data['msg error'] = 'Method not allowed'

    # jsonify: convierte la salida JSON en un objeto Response con
    # la aplication/json mimetype
    result = jsonify(data)

    # Se modifica el código de estado de la respuesta a 404
    # 404: Recurso no encontrado, el servidor web no encuentra la página
    # http://docs.python-requests.org/en/master/user/quickstart/
    result.status_code = 405

    # Añadimos mensaje para comprobar que se ha producido un 'method not allowed'
    logger.error("405 Method not allowed - Status 405")

    return result # devolvemos { "msg error": "Method not allowed" }

# ---------------------------------------------------------------------------- #

# Función para visualizar todos los elementos (MÉTODO GET)
# GET para obtener un recurso del servidor
# curl -i http://127.0.0.1:5000/data_twitter
@app.route('/data_twitter', methods=['GET'])
def get_all_data():

    data = {} # definimos un diccionario
    # No hace falta añadir al diccionario --> data['status'] = 'OK'
    data['ruta'] = request.url # obtener la url de la petición
    data['valor'] = data_twitter

    # jsonify: convierte la salida JSON en un objeto Response con
    # la aplication/json mimetype
    result = jsonify(data)

    # Se modifica el código de estado de la respuesta a 200
    # 200: Respuesta estándar para peticiones correctas
    result.status_code = 200

    # Añadimos mensaje cuando se visualicen todos los items
    logger.info("Successfully method GET: The URL shows all the items in '/data_twitter' - Status 200")

    return result

# ---------------------------------------------------------------------------- #

# Función para visualizar un solo un elemento del JSON (MÉTODO GET)
# GET para obtener un recurso del servidor
# curl -i http://127.0.0.1:5000/data_twitter/<name>
@app.route('/data_twitter/<nameID>', methods=['GET'])
def get_data(nameID):

    data = {} # definimos un diccionario
    # No hace falta añadir al diccionario --> data['status'] = 'OK'
    data['ruta'] = request.url # obtener la url de la petición
    data['valor'] = [ elem for elem in data_twitter if (elem['name'] == nameID) ]

    # jsonify: convierte la salida JSON en un objeto Response con
    # la aplication/json mimetype
    result = jsonify(data)

    # Se modifica el código de estado de la respuesta a 200
    # 200: Respuesta estándar para peticiones correctas
    result.status_code = 200

    # Añadimos mensaje cuando se visualice un item
    logger.info("Successfully method GET: The URL shows only one item in '/data_twitter/%s' - Status 200", nameID)

    return result

# ---------------------------------------------------------------------------- #

# Función para crear un nuevo elemento (MÉTODO PUT)
# PUT para crear un recurso del servidor
# curl -i -X PUT http://127.0.0.1:5000/data_twitter
@app.route('/data_twitter', methods=['PUT'])
def put_data():

    # Nos creamos un nuevo elemento
    new_data = {
                "name": "hola",
                "url": "hola.es",
                "query": "hola",
                "tweet_volume": "1234567"
                }

    # Añadimos el nuevo elemento al conjunto de elementos
    data_twitter.append(new_data)

    data = {} # definimos un diccionario
    # No hace falta añadir al diccionario --> data['status'] = 'OK'
    data['ruta'] = request.url # obtener la url de la petición
    data['valor'] = new_data

    # jsonify: convierte la salida JSON en un objeto Response con
    # la aplication/json mimetype.
    result = jsonify(data)

    # Se modifica el código de estado de la respuesta a 200
    # 200: Respuesta estándar para peticiones correctas
    result.status_code = 200

    # Añadimos mensaje cuando se cree un nuevo item
    logger.info("Successfully method PUT: The URL shows the creation of the new item in '/data_twitter' - Status 200")

    return result

# ---------------------------------------------------------------------------- #

# Función para modificar elemento
# POST para actualizar un recurso del servidor
# curl -i -X POST http://127.0.0.1:5000/data_twitter/Bernabeu
@app.route('/data_twitter/<nameID>', methods=['POST'])
def post_data(nameID):

    data_json = [ elem for elem in data_twitter if (elem['name'] == nameID) ]

    if "name" in request.args:
        data_json[0]['name'] = request.args['name']

    if "tweet_volume" in request.args:
        data_json[0]['tweet_volume'] = request.args['tweet_volume']

    data = {} # definimos un diccionario
    # No hace falta añadir al diccionario --> data['status'] = 'OK'
    data['ruta'] = request.url # obtener la url de la petición
    data['valor'] = data_json[0]

    # jsonify: convierte la salida JSON en un objeto Response con
    # la aplication/json mimetype.
    result = jsonify(data)

    # Se modifica el código de estado de la respuesta a 200
    # 200: Respuesta estándar para peticiones correctas
    result.status_code = 200

    # Añadimos mensaje cuando se modifique item
    logger.info("Successfully method POST: The URL shows the modification of the item in '/data_twitter/%s' - Status 200", nameID)

    return result

# ---------------------------------------------------------------------------- #

# Función para eliminar un elemento (MÉTODO DELETE)
# DELETE para eliminar un recurso del servidor
# curl -i -X DELETE http://127.0.0.1:5000/data_twitter/Bernabeu
@app.route('/data_twitter/<nameID>', methods=['DELETE'])
def delete_data(nameID):

    data_delete = [ elem for elem in data_twitter if (elem['name'] == nameID) ]

    if len(data_delete) == 0:

        data = {} # definimos un diccionario
        data['msg error'] = 'URL not found'

        # jsonify: convierte la salida JSON en un objeto Response con
        # la aplication/json mimetype
        result = jsonify(data)

        # Se modifica el código de estado de la respuesta a 404
        # 404: Recurso no encontrado, el servidor web no encuentra la página
        # http://docs.python-requests.org/en/master/user/quickstart/
        result.status_code = 404

        # Añadimos mensaje para comprobar que se ha desplegado de forma incorrecta
        log.error("404 Not Found: The requested URL was not found on the server.")

        return result # devolvemos { "msg error": "URL not found" }

    data_twitter.remove(data_delete[0])

    data = {} # definimos un diccionario
    # No hace falta añadir al diccionario --> data['status'] = 'OK'
    data['ruta'] = request.url # obtener la url de la petición
    data['valor'] = "Deleted"

    # jsonify: convierte la salida JSON en un objeto Response con
    # la aplication/json mimetype
    result = jsonify(data)

    # Se modifica el código de estado de la respuesta a 200
    # 200: Respuesta estándar para peticiones correctas
    result.status_code = 200

    # Añadimos mensaje cuando se elimine un item
    logger.warning("Successfully method DELETE: The URL shows the deletion of an item in '/data_twitter/%s' - Status 200", nameID)

    return result

# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port,debug=True)
    #app.run(debug=True, port = 5000)
