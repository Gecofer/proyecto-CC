# ---------------------------------- main.py --------------------------------- #

# Autora: Gema Correa Fernández

'''
Fichero que implementa la clase API REST haciendo uso del microframework Flask
'''


# Bibliotecas a usar
from flask import Flask     # importamos la clase Flask
from flask import jsonify   # https://pypi.org/project/Flask-Jsonpify/
from flask import request   # https://github.com/requests/requests

import os
from data import *

# Creación de una instancia de la clase Flask
app = Flask(__name__)


# ---------------------------------------------------------------------------- #

# Obtenemos los datos
try:
    with open('data/data.json', encoding='utf-8') as data_file:
        data_twitter = json.loads(data_file.read())
except IOError as fail:
    print("Error %d reading %s", fail.errno, fail.strerror)

# ---------------------------------------------------------------------------- #

# Ruta para comprobar que se ha desplegado de forma correcta
@app.route('/')
@app.route('/status')
def index():
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

    return result # devolvemos { "msg error": "Method not allowed" }

# ---------------------------------------------------------------------------- #

    # Función para visualizar un solo un elemento del JSON (MÉTODO GET)
    # GET para obtener un recurso del servidor
    # Ejemplo: http://127.0.0.1:5000/get_data?id=GR
    @app.route('/get_data', methods=['GET'])
    def get_data():
        if 'id' in request.args:

            # Si está el ID, muestra el elemento correspondiente
            if request.args['id'] in data_twitter:
                data = {} # definimos un diccionario
                # No hace falta añadir al diccionario --> data['status'] = 'OK'
                data['ruta'] = request.url # obtener la url de la petición
                data['valor'] = get_id_data_twitter(request.args['id'])

                # jsonify: convierte la salida JSON en un objeto Response con
                # la aplication/json mimetype.
                result = jsonify(data)

                # Se modifica el código de estado de la respuesta a 200
                # 200: Respuesta estándar para peticiones correctas
                result.status_code = 200

                return result

            else: # Si no está el ID
                data = {} # definimos un diccionario
                data['msg error'] = 'URL not found'

                # jsonify: convierte la salida JSON en un objeto Response con
                # la aplication/json mimetype.
                result = jsonify(data)

                # Se modifica el código de estado de la respuesta a 200
                # 404: Recurso no encontrado, el servidor web no encuentra la página
                result.status_code = 404

                return result

        else: # Si no sabemos como escribirlo
            data = {} # definimos un diccionario
            data['msg error'] = 'URL not found'

            # jsonify: convierte la salida JSON en un objeto Response con
            # la aplication/json mimetype.
            result = jsonify(data)

            # Se modifica el código de estado de la respuesta a 200
            # 404: Recurso no encontrado, el servidor web no encuentra la página
            result.status_code = 404

            return result

# ---------------------------------------------------------------------------- #

    # Función para visualizar todos los elementos (MÉTODO GET)
    @app.route('/data_twitter', methods=['GET'])
    def get_all_data():

        # GET para obtener un recurso del servidor
        if request.method == 'GET':
            data = {} # definimos un diccionario
            # No hace falta añadir al diccionario --> data['status'] = 'OK'
            data['ruta'] = request.url # obtener la url de la petición
            data['valor'] = get_data_twitter()

            # jsonify: convierte la salida JSON en un objeto Response con
            # la aplication/json mimetype
            result = jsonify(data)

            # Se modifica el código de estado de la respuesta a 200
            # 200: Respuesta estándar para peticiones correctas
            result.status_code = 200

            return result

# ---------------------------------------------------------------------------- #

    # Función para crear un nuevo elemento
    # PUT para crear un recurso del servidor
    # curl -i http://127.0.0.1:5000/data_twitter
    @app.route('/data_twitter', methods=['PUT'])
    def put_data():

        if request.method == 'PUT':

            # Nos creamos un nuevo elemento
            new_data = {"ML": [{ "name":"Malaga",
                         "url_twitter":"https://twitter.com/malaga",
                         "user_twitter":"@malaga"
                        }]}

            # Añadimos el nuevo elemento al conjunto de elementos
            new_data_twitter = add_data_twitter(new_data)

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

            return result

# ---------------------------------------------------------------------------- #

    # Función para modificar elemento
    @app.route('/data_twitter', methods=['POST'])
    def post_data():

        # POST para actualizar un recurso del servidor
        # En este caso modificamos el valor del usuarios
        # curl -X POST http://127.0.0.1:5000/data_twitter?id=GR
        if request.method == 'POST':

            if 'id' in request.args:
                update_data_twitter(request.args['id'], "name", "SEVILLA")

                data = {} # definimos un diccionario
                # No hace falta añadir al diccionario --> data['status'] = 'OK'
                data['ruta'] = request.url # obtener la url de la petición
                data['valor'] = get_id_data_twitter(request.args['id'])

                # jsonify: convierte la salida JSON en un objeto Response con
                # la aplication/json mimetype.
                result = jsonify(data)

                # Se modifica el código de estado de la respuesta a 200
                # 200: Respuesta estándar para peticiones correctas
                result.status_code = 200

                return result

            else: # Si no está el ID
                data = {} # definimos un diccionario
                data['msg error'] = 'URL not found'

                # jsonify: convierte la salida JSON en un objeto Response con
                # la aplication/json mimetype.
                result = jsonify(data)

                # Se modifica el código de estado de la respuesta a 200
                # 404: Recurso no encontrado, el servidor web no encuentra la página
                result.status_code = 404

                return result

# ---------------------------------------------------------------------------- #

    # Función para eliminar un elemento
    @app.route('/data_twitter', methods=['DELETE'])
    def delete_data():

        # -------------------------------------------------------------------  #
        # DELETE para eliminar un recurso del servidor
        #  curl -X DELETE http://127.0.0.1:5000/data_twitter?id=GR
        if request.method == 'DELETE':
            if 'id' in request.args:
                remove_data_twitter(request.args['id'])

                data = {} # definimos un diccionario
                # No hace falta añadir al diccionario --> data['status'] = 'OK'
                data['ruta'] = request.url # obtener la url de la petición
                data['valor'] = get_id_data_twitter(request.args['id'])

                # jsonify: convierte la salida JSON en un objeto Response con
                # la aplication/json mimetype.
                result = jsonify(data)

                # Se modifica el código de estado de la respuesta a 200
                # 200: Respuesta estándar para peticiones correctas
                result.status_code = 200

                return result

            else: # Si no sabemos como escribirlo
                # aqui debe devolver ERROR
                data = {} # definimos un diccionario
                data['msg error'] = 'URL not found'

                # jsonify: convierte la salida JSON en un objeto Response con
                # la aplication/json mimetype.
                result = jsonify(data)

                # Se modifica el código de estado de la respuesta a 200
                # 404: Recurso no encontrado, el servidor web no encuentra la página
                result.status_code = 404

                return result

# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port,debug=True)
    app.run(debug=True, port = 5000)
