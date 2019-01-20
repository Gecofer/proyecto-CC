## Documentar avances o mejoras del proyecto

**Tabla de Contenidos**

- [Hito 3](#id0)
  - [Avance 1](#id1)
  - [Avance 2](#id2)
  - [Avance 3](#id3)
  - [Avance 4](#id4)
- [Hito 4](#id5)
  - [Avance 1](#id6)
  - [Avance 2](#id7)
- [Hito 5](#id8)

### Hito 3 <a name="id0"></a>

#### Avance 1 <a name="id1"></a>

Se ha hecho uso de un conjunto de datos (tendencias) procedentes de la API de Twitter (todo documentado en la [carpeta data](https://github.com/Gecofer/proyecto-CC/tree/master/data)). Para ello, lo primero que hemos hecho ha sido obtener unas claves de acceso para Twitter, las cuales se obtienen accediendo a la página [Twitter Aps](https://apps.twitter.com), creando una nueva app y obteniendo las claves siguientes:

- _Consumer Key (API Key)_
- _Consumer Secret Key (API Secret)_
- _Access Token_
- _Access Token Secret_

![](images/claves_twitter.png)

Para hacer un uso correcto de estas claves de acceso privadas, es aconsejable ponerlas como variables de entorno en nuestro bash, realizando un export [[1][1]], y en nuestro código `twitterAPI.py` (pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/data/twitterAPI.py) para verlo):

~~~
auth = tweepy.OAuthHandler(environ["TWITTER_CONSUMER_KEY"],
                          environ["TWITTER_CONSUMER_SECRET"])

auth.set_access_token(environ["TWITTER_ACCESS_TOKEN"],
                      environ["TWITTER_ACCESS_TOKEN_SECRET"])
~~~

Una vez que ya tenemos acceso a la API, se realiza la función `API.trends_place(id[, exclude])` [[4][4]], que devuelve las 10 tendencias virales en formato JSON. (_Esta información se almacena en caché durante 5 minutos. Solicitar con frencuencia no devolverá más datos y contará en contra de su límite de uso, es por eso que es aconsejable ralizar pocas solicitudes y guardarlo en un archivo._)


[1]: https://github.com/lauramayol/laura_python_core/blob/b0f62fb70ecef0e8f3d5e8476665a48519dfc44e/week_05/mini_projects/api_from_other_apis/tweet.py


#### Avance 2 <a name="id2"></a>

La creación del conjunto de datos obtenidos de la API de Twitter, ha llevado a eliminar el fichero `util.py` y su correspondiente test `util_test.py`, el cual me permitía manejar una estructura de datos sencilla para el desarrollo del hito 2:

~~~
data_twitter = {
    "GR": [
            {
                "name":"Granada",
                "url_twitter":"https://twitter.com/aytogr?lang=es",
                "user_twitter":"@aytogr"
            },
        ]
    ,

    "MDR": [
            {
                "name":"Madrid",
                "url_twitter":"https://twitter.com/madrid",
                "user_twitter":"@MADRID"
            },
        ]
    ,

    "VLC": [
            {
                "name":"Valencia",
                "url_twitter":"https://twitter.com/ajuntamentvlc?lang=es",
                "user_twitter":"@AjuntamentVLC",
            },
        ]
}

# ---------------------------------------------------------------------------- #
# Función que devuelve todos los valores de la variable "data_twitter"
def get_data_twitter():
    return data_twitter
# ---------------------------------------------------------------------------- #
# Función que devuelve uno de los valores de la variable "data_twitter"
def get_id_data_twitter(data):
    if data in data_twitter:
        return data_twitter[data]
    else:
        return False
# ---------------------------------------------------------------------------- #
# Función que modificar uno de los atributos de la variable "data_twitter"
def update_data_twitter(data, name, user):
    if data in data_twitter:
        data_twitter[data][0][name] = user
        return True
    else:
        return False
# ---------------------------------------------------------------------------- #
....
~~~

#### Avance 3 <a name="id3"></a>

El fichero `main.py` ha sufrido diversas modificaciones (pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/main.py) para acceder al mismo):

  1. Realizamos una lectura del JSON obtenido en el avance 1:

  ~~~
  try:
    with open('data/data.json', encoding='utf-8') as data_file:
        data_twitter = json.loads(data_file.read())
  except IOError as fail:
    print("Error %d reading %s", fail.errno, fail.strerror)
  ~~~

  2. Para comprobar que se ha desplegado de forma correcta, disponemos de dos rutas:

  ~~~
  @app.route('/')
  @app.route('/status')
  ~~~

  3. La función `get_data(nameID)` creada para visualizar un solo un elemento del JSON (método GET para obtener un recurso del servidor), ha sufrido modificaciones, debido a que en el anterior hito se accedía de la forma `/get_data?id=GR` y ahora se ha modificado a `/data_twitter/<nameID>`, lo que ha llevado una modificación del código.

  4. La función `post_data(nameID)` creada para modificar un elemento del JSON (método POST para actualizar un recurso del servidor), ha sufrido modificaciones, debido a que en el anterior hito se accedía de la forma `/get_data?id=GR` y ahora se ha modificado a `/data_twitter/<nameID>`, lo que ha llevado una modificación del código.

  5. La función `delete_data(nameID)` creada para eliminar un elemento del JSON (método DELETE para eliminar un recurso del servidor), ha sufrido modificaciones, debido a que en el anterior hito se accedía de la forma `/get_data?id=GR` y ahora se ha modificado a `/data_twitter/<nameID>`, lo que ha llevado una modificación del código.

  6. Se ha cambiado la forma de acceder al puerto que por defecto usa Flask, para que en el despliegue en Azure se pueda acceder al puerto 80.

  ~~~
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=True)
  #app.run(debug=True, port = 5000)
  ~~~

#### Avance 4 <a name="id4"></a>

La modificación del fichero `main.py`, ha supuesto realizar algunos cambios en su fichero de testeo `main_test.py`. Además, se han realizado dos funciones nuevas de test, una de ellas comprueba que Flask ha arrancado bien y la otra comprueba que nos hemos equivocado al escribir la URL. Con ello, lo que estamos haciendo es tener cada vez un código más robusto.

### Hito 3 <a name="id5"></a>

#### Avance 1 <a name="id6"></a>

Se ha incorporado a nuestro proyecto, un sistema centralizado de logs, que tendremos que tener en cuenta cada vez que creemos o mdodifiquemos un fichero. Un log ("registro", en español) es un archivo de texto en el que constan cronológicamente los acontecimientos que han ido afectando a un sistema informático (programa, aplicación, servidor, etc.), así como el conjunto de cambios que estos han generado [[1][1]]. Básicamente los logs, nos van a permitir tener un mayor control del de la información, con el fin de detectar más rápidamente posibles fallos.

Para este servicio que estamos implementando, utilizaremos la biblioteca de generación de logs de Python ([logging](https://docs.python.org/3.6/library/logging.html)). Este módulo define funciones y clases que implementan un sistema flexible de registro de eventos para aplicaciones y bibliotecas. La ventaja clave de tener la API de registro proporcionada por un módulo de biblioteca estándar es que todos los módulos de Python pueden participar en el registro, de modo que el registro de su aplicación puede incluir sus propios mensajes integrados con mensajes de módulos de terceros.

Dicho registro se registrará en un fichero llamado `debug.log`. Por tanto, vamos a ver las modificaciones hechas en nuestro código:

1. Importamos el módulo.

  ~~~
  import logging
  ~~~

2. Devolvemos un _logger_ con el nombre especificado o, si el nombre es ninguno, devuelve un logger que sea el logger raíz de la jerarquía. Si se especifica, el nombre es típicamente un nombre jerárquico separado por puntos como

  ~~~
  logger = logging.getLogger("app")
  ~~~

3. Se realiza la configuración básica del sistema de registro creando un _StreamHandler_ con un formato predeterminado y añadiéndolo al registrador raíz. Las funciones debug(), info(), warning(), error() y critical() llamarán a basicConfig() automáticamente si no se definen handlers para el registrador raíz. Además, establecemos que nos muestre la traza del nivel de debug() o superior.

  ~~~
  logging.basicConfig(filename= "debug.log", filemode='a', format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
  ~~~

  Vamos a entender que significan cada uno de los niveles disponibles para identificación de logs [[2][2]]:

  - DEBUG: Información que es diagnósticamente útil para la gente más allá de los desarrolladores (IT, administradores de sistemas, etc.).
  - INFO: Información general útil para registrar (inicio/parada de servicio, supuestos de configuración, etc.). Información que quiero tener siempre disponible, pero que por lo general no me importa en circunstancias normales.
  - WARNING: Cualquier cosa que potencialmente pueda causar rarezas de aplicación, pero para la cual me estoy recuperando automáticamente. (Por ejemplo, cambiar de un servidor primario a un servidor de copia de seguridad, volver a intentar una operación, falta de datos secundarios, etc.).
  - ERROR: Cualquier error que sea fatal para la operación, pero no para el servicio o la aplicación (no se puede abrir un archivo requerido, falta de datos, etc.). Estos errores obligarán al usuario (administrador o usuario directo) a intervenir. Estos son usualmente reservados (en mis aplicaciones) para cadenas de conexión incorrectas, servicios faltantes, etc.
  - FATAL: Cualquier error que obligue a cerrar el servicio o la aplicación para evitar la pérdida de datos (o una mayor pérdida de datos). Me reservo estos sólo para los errores más atroces y las situaciones en las que se garantiza que ha habido corrupción o pérdida de datos.


4. Añadiremos el log con la información que deseemos, como por ejemplo:

  ~~~
  logger.error("404 Not Found: The requested URL was not found on the server - Status 404")
  ~~~

Se debe tener en cuenta, que la creación de un registro conlleva una consistencia, por lo que se deberá siempe seguir la misma estructura para dicho registro. Por tanto, hemos hecho las anteriores modificaciones en los siguientes microservicios:  

- Se han añadido logs a la conexión y descarga de datos procedentes de la API de Twitter como viemos [aquí](https://github.com/Gecofer/proyecto-CC/tree/master/data), con el fin de saber cuando nos conectamos a la API de Twitter y cuando obtenemos los datos. a continuación, se ve una salida:


~~~
2018-12-18 02:19:10,761 - data - INFO - Successfully connected API Twitter.
2018-12-18 02:19:10,761 - tweepy.binder - DEBUG - PARAMS: {'lat': b'37.1833', 'long': b'-3.6'}
2018-12-18 02:19:10,762 - requests_oauthlib.oauth1_auth - DEBUG - Signing request <PreparedRequest [GET]> using client
2018-12-18 02:19:10,762 - requests_oauthlib.oauth1_auth - DEBUG - Including body in call to sign: False
2018-12-18 02:19:11,123 - requests_oauthlib.oauth1_auth - DEBUG - Updated body: None
2018-12-18 02:19:11,124 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): api.twitter.com:443
2018-12-18 02:19:11,463 - urllib3.connectionpool - DEBUG - https://api.twitter.com:443 "GET /1.1/trends/place.json?id=766356 HTTP/1.1" 200 5268
2018-12-18 02:19:11,466 - data - INFO - Successfully obtain location trends.
~~~

- Se ha añadido un sistema de logs a nuestro microservicio de Flask, con el fin de saber nos conectamos, que salidas recibimos. Hay que tener en cuenta que Flask cuenta con su propio sistema de logs, por lo que veremos la salida de los logs creados por nosotros mismos y por Flask:

~~~
2018-12-18 02:23:00,324 - werkzeug - WARNING -  * Debugger is active!
2018-12-18 02:23:00,340 - werkzeug - INFO -  * Debugger PIN: 103-029-300
2018-12-18 02:23:05,350 - app - INFO - Successfully status application in '/' or '/status'
2018-12-18 02:23:05,350 - werkzeug - INFO - 127.0.0.1 - - [18/Dec/2018 02:23:05] "GET / HTTP/1.1" 200 -
2018-12-18 02:23:21,900 - app - INFO - Successfully method GET: The URL shows all the items in '/data_twitter' - Status 200
2018-12-18 02:25:17,907 - app - ERROR - 404 Not Found: The requested URL was not found on the server - Status 404
2018-12-18 02:25:17,908 - werkzeug - INFO - 127.0.0.1 - - [18/Dec/2018 02:25:17] "GET /data_twitt HTTP/1.1" 404 -
~~~

Esta mejora supone un avance sustancial en nuestro servicio, debido a que ahora tenemos un registro de todo nuestro proyecto, con el fin de detectar errores que antes no eran más difíciles de encontrar. Además, la incorporación de un sistema de logs, se puede realizar de muchas maneras, aquí muestro una serie de tutoriales bastantes interesantes:

- [logging — Logging facility for Python](https://docs.python.org/3/library/logging.html)
- [Logging in Python](https://realpython.com/python-logging/)
- [Good logging practice in Python](https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/)
- [Logging en Python (un tutorial frustrado)](https://moduslaborandi.net/post/python-logging/)
- [Logging in Flask](http://flask.pocoo.org/docs/1.0/logging/)
- [Aprende Python en 5 días](https://ricveal.com/blog/curso-python-5/)
- [Logs en Flask](http://lineadecodigo.com/python/logs-en-flask/)


#### Avance 2 <a name="id7"></a>

La incorporación de un sistema centralizado de logs, ha llevado a cabo una revisión del código que testea nuestro proyecto. Asimismo como una reestructuración de la documentación disponible en Github.


### Hito 5 <a name="id8"></a>


[1]: https://dbi.io/es/blog/que-son-los-logs/
[2]: https://stackoverflow.com/questions/2031163/when-to-use-the-different-log-levels
