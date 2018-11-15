## Título del proyecto

Análisis de datos (geolocalizados) en Twitter.

## Descripción del proyecto

Twitter junto con Instagram son dos de las plataformas sociales más usadas actualmente, por eso mismo, miles de usuarios comparten todo tipo de información en ellas. Este tipo de comportamientos benefician a las empresas dándoles potestad en la obtención de información muy valiosa, cómo por ejemplo ver qué _trending topics_ son los más comentados o qué ciudades son las más comentadas en la red. En este caso, yo me voy a centrar en la obtención de datos geolocalizados mediante _trending topics_ que usan los usuarios en Twitter. Entonces, el objetivo del proyecto es poder clasificar las tendencias por ubicaciones, para así establecer la tendencia mayoritaria en una region determinada, la cual abarcará más de una localización.

La API de Twitter nos permite acceder a toda esa información de forma más simple que la de Instagram, es por eso que me he decantado por esta red social. A continuación, se muestran algunos datos a los que podemos acceder [[1][1]]:

- __Tweets__: búsqueda, publicación, filtrado, etc.
- __Anuncios__: gestión de campañas, análisis, etc.
- __Contenido multimedia__: subir y acceder a fotos, vídeos, GIF animados, etc.
- __Tendencias__: _trending topics_.
- __Geo__: información sobre lugares conocidos, lugares cerca de una ubicación, etc.


## Arquitectura software

Actualmente, las arquitecturas software modernas buscan la consistencia en la velocidad de respuesta al usuario. Sin embargo, en el mercado existen muchos tipos de arquitecturas, es por ello que a veces se hace difícil concretar qué arquitectura se va a utilizar [[2][2]]:

- __Arquitectura en capas__: arquitectura cliente-servidor, tiene 3 o más capas, normalmente se suelen incluir la capa de presentación, la de aplicación, la de lógica de negocio y la de acceso a datos. El problema principal es que solo permite escalado dentro de cada una de las capas, siendo al final alguna de ellas un cuello de botella.
- __Arquitectura dirigida por eventos__: tiene una cola de eventos que se originan en el usuario, pero también de una parte a otra de la arquitectura. Es difícil de testear y su desarrollo es más complicado que la anterior.
- __Arquitectura microkernel__: arquitectura casi monolítica, con un núcleo central al que se pueden añadir funcionalidades mediante _plugins_, siendo su problema principal la escalabilidad, ya que el núcleo puede representar un cuello de botella.
- __Arquitectura basada en microservicios__: arquitectura muy popular hoy en día, se caracteriza por poder usar unidades que se van a desplegar de forma independiente y por poder usar tecnologías subyacentes que van desde la virtualización completa en la nube hasta el uso de contenedores _Docker_ en una sola máquina virtual.
- __Arquitectura basada en espacios__: arquitectura antigua, de la década de los 90.

Entonces, resulta bastante claro que de todas las comentadas anteriormente vayamos a hacer uso de la __arquitectura basada en microservicios__, ya que es la que más actual y la que menos problemas presenta, además de que nos permite tener diferentes servicios trabajando de forma totalmente independiente unos de otros.

### Microservicios a desarrollar

Para realizar la arquitectura se va a hacer uso del lenguaje [Python](https://www.python.org), y para el desarrollo de los microservicios se puede usar cualquier microframework web para Python, en este caso existe la posibilidad de usar [Django](https://www.djangoproject.com) (más complejo o pensado para un proyecto de grandes dimensiones o que crezca) o [Flask](http://flask.pocoo.org) (más sencillo). Es por ello, que tras haber buscado documentación, hablado con usuarios de ambos microframework y ser la primera vez que uso este tipo de tecnología, me he decantado por Flask.

<p align="center">
  <img width="250" height="100" src="images/twitter+python.png">
</p>

Los microservicios previstos a desarrollar son los siguientes:

<p align="center">
  <img width="460" height="370" src="images/estructura_microservicios.png">
</p>

1. __Consultar API de Twitter__: en este microservicio solo nos vamos a centrar en acceder, consultar y bajarnos información de la API, información obtenida en un [JSON](https://www.json.org).
2. __Procesar información__: en este microservicio vamos a quedarnos con los datos referentes a las tendencias según su localización, en un JSON: [`API.trends_place(id[, exclude])`](http://docs.tweepy.org/en/v3.5.0/api.html).
3. __Almacenar información__: en este microservicio nos vamos a centrar en crear una estructura para los datos que hemos realizado, usando principalmente una BD como [MongoDB](https://www.mongodb.com/es).
4. __Mostrar información__: en este microservicio solo nos interesa mostrar la información relevante de alguna manera específica.

Además, necesitamos un sistema de centralización de [__logs__](https://www.elastic.co/products/logstash), al cual todos deben comunicarse.

### Comunicación entre los microservicios

La comunicación entre servicios será realizada por _brokers_, en concreto con [RabbitMQ](https://www.rabbitmq.com), que es un sistema de manejo de colas.

### Bibliotecas de Python para la API de Twitter

Python cuenta muchas bibliotecas desarrolladas para la API de Twitter. Sin embargo, al no haber usado nunca ninguna me es dífil elegir que biblioteca es la mejor. Es por ello, que voy hacer uso de [tweepy](https://github.com/tweepy/tweepy) ya que he oído hablar de ella bastante bien y tiene bastante documetación en la web. De todas maneras, existen otras librerías cómo [twython](https://github.com/ryanmcgrath/twython), [python-twitter](https://github.com/bear/python-twitter) o [TwitterAPI](https://github.com/geduldig/TwitterAPI).

### Tests en Python (código sin test código roto)

Para testear en Python [[3][3]], puedo usar algunas de las librerías que me permiten implementar pruebas unitarias en dicho lenguaje como [unittest](https://docs.python.org/3.5/library/unittest.html), [doctest](https://docs.python.org/3.5/library/doctest.html) o [pytest](https://docs.pytest.org/en/latest/) [[4][4]]. En este caso yo voy hacer uso de la biblioteca [unittest](https://docs.python.org/3.5/library/unittest.html), ya que nos ofrece toda la potencia del lenguaje para probar nuestros programas, lo que significa que ayuda a determinar rápidamente el impacto de cualquier modificación en el resto del código.

Para realizar la configuración de los test correctamente, voy hacer uso de [Travis CL](https://www.travis-ci.org), que es un sistema distribuido de generación e integración continua libre, que me permite conectar mi repositorio de Github y testear después de cada push que haga [[5][5]] [[6][6]]. En el apartado siguiente, explico como establecer el testeo con travis, cuando quiero desplegar.

Por tanto, para establecer un testeo cada vez que haga `git push`, he seguido el [tutorial de Travis](https://docs.travis-ci.com/user/tutorial/):

### Despliegue

#### PaaS

Cuando se quiere desplegar una aplicación sobre una infraestructura ya definida y que no va a cambiar se necesita un _Platform as a Service_ o PaaS. Entre los posibles servicios que hay [Heroku](https://www.heroku.com) o [OpenShift](https://www.openshift.com), vamos a escoger [Heroku](https://www.heroku.com), ya que es un servicio fiable, gratuito, ofrece muchas opciones a la hora de elegir el lenguaje y permite integrar Github con Travis.

Despliegue: https://glacial-castle-84194.herokuapp.com

#### Rutas utilizadas en la aplicación

- _/_: devuelve el JSON {"status":"OK"} (https://glacial-castle-84194.herokuapp.com).
- _error en la ruta_: devuelve el JSON {"msg error":"URL not found"} (https://glacial-castle-84194.herokuapp.com/get_dat)
- _/get_data_: lista un solo un elemento del JSON mediante el método GET, el cual obtiene un recurso del servidor (https://glacial-castle-84194.herokuapp.com/get_data?id=GR)
- _/data_twitter_ con GET: lista todos los elementos del JSON (https://glacial-castle-84194.herokuapp.com/data_twitter)
- _/data_twitter_ con PUT: crea un nuevo usuario _(curl -i -X PUT https://glacial-castle-84194.herokuapp.com/data_twitter)_ y para comprobar que se ha creado _(curl -i https://glacial-castle-84194.herokuapp.com/data_twitter)_
- _/data_twitter_ con POST: modifica un nuevo usuario_(curl -X POST https://glacial-castle-84194.herokuapp.com/get_data?id=GR)_
- _/data_twitter_ con DELETE: elimina un usuario _(curl -X DELETE http://127.0.0.1:5000/data_twitter?id=GR)_

### Ficheros usados

- _main.py_: fichero que implementa la clase API REST haciendo uso del microframework Flask
- _test/main_test.py_:
- _util.py_: fichero que contiene la información a mostrar en la clase TwitterData
- _test/util_test.py_:

### Pasos para hacer el despliegue

1. Identificarse en Travis mediante Github.

2. Añadir un archivo __[.travis.yml](https://github.com/Gecofer/proyecto-CC/blob/master/.travis.yml)__ al repositorio para decirle a Travis CI qué hacer, el cual contiene :
  *  El lenguaje del programación y la versión usada. En este caso he hecho uso de Python 3.7.0 para OSX.
  *  El comando para instalar las dependencias, el cual contiene las dependencias a instalar.
  *  El comando para ejecutar los tests.

3. Habilitar el repositorio en Travis, para así cada vez que se haga `git push` se compilen en Travis. Para ello, una vez iniciado sesión en Travis mediante Github, tengo que seleccionar la pestaña del repositorio que quiero ejecutar.

<p align="center">
  <img width="700" height="100" src="images/travis.png">
</p>

4. Crear cuenta en Heroku.

5. Instalar el comando de [Heroku Command Line Interface (CLI)](https://devcenter.heroku.com/articles/getting-started-with-python#set-up). _Como anotación comentar que cada semana actualizan la versión._

6. Identificarse introduciendo nuestras credenciales de la cuenta de Heroku: `heroku login`

7. Para que Heroku pueda encontrar el archivo principal del proyecto, debemos definirnos un archivo __Procfile__ en Heroku [[7][7]] que contendrá la siguiente instrucción `web: gunicorn main:app`, usaremos [gunicorn](https://gunicorn.org) ya que nos permite administrar las peticiones simultaneas que nuestra aplicación reciba

8. Creo el fichero __requirements.txt__, para instalar las dependencias. Este fichero se puede instalar de diversas formas, no es recomendable usar  `pip freeze > __requirements.txt`, ya que te mete basura [[8][8]]. Debemos recordar añadir _gunicorn_.

9. Crear el fichero __runtime.txt__, en mi caso la versión de Python 3.7.0.

10. Crear una aplicación en Heroku, este proceso se puede hacer de dos maneras: por terminal `heroku create` o mediante la web _Create new App_.

11. Configuar el despliegue automático asociando la aplicación de Heroku con nuestra cuenta de GitHub.

  * En web, accedemos a la aplicacion creada y buscamos _Deploy_
  * Seleccionamos GitHub como _Deployment method_
  * Conectamos la app en introduciendo nuestra datos de GitHub
  * Indicamos el repositorio de GitHub de nuestra aplicación
  * Activamos los despliegues automáticos y que Travis ejecute antes de desplegar.

  <p align="center">
    <img width="600" height="500" src="images/deploy_heroku.png">
  </p>

11. `git push heroku master`

12. `git push`

## Licencia

Proyecto bajo licencia (GNU GLP V3)[https://github.com/Gecofer/proyecto-CC/blob/master/LICENSE].

[1]: https://stackabuse.com/accessing-the-twitter-api-with-python/
[2]: https://github.com/JJ/CC/blob/master/documentos/temas/Arquitecturas_para_la_nube.md
[3]: https://github.com/JJ/tests-python
[4]: https://recursospython.com/guias-y-manuales/unit-testing-doc-testing/
[5]: https://www.smartfile.com/blog/testing-python-with-travis-ci/
[6]: https://github.com/softwaresaved/build_and_test_examples
[7]: https://devcenter.heroku.com/articles/getting-started-with-python
[8]: https://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/

## Enlaces de Interés  

- [Publics APIs](https://github.com/toddmotto/public-apis#books)

__Nota__: _Se debe tener en cuenta que la realización de un proceso de desarrollo conlleva modificaciones en el futuro, pudiendo modificar la documentación o añadiendo nuevas funcionalidades._
