## Documentar avances o mejoras del proyecto

**Tabla de Contenidos**

- [Hito 3](#id0)
  - [Avance 1](#id1)
  - [Avance 2](#id2)
  - [Avance 3](#id3)
  - [Avance 4](#id4)

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
