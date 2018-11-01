# Proyecto Cloud Computing 2018-2019

Se puede consultar también la información en el siguiente enlace.

## Título del proyecto

Análisis de las imágenes geolocalizadas en Twitter.

## Descripción del proyecto

Twitter junto con Instagram son dos de las plataformas sociales más usadas actualmente, por eso mismo, miles de usuarios comparten sus fotografías en ellas. Este tipo de comportamientos benefician a las empresas con la obtención de información muy diversa, cómo por ejemplo ver que ciudades son las más comentadas en la red. En este caso, yo me voy a centrar en las imágenes geolocalizadas que suben los usuarios a Twitter, para así luego poder clasificar que localizaciones son las más mencionadas. Sin embargo, debemos tener en cuenta que esas imágenes pueden estar localizadas tanto por la ubicación de Twitter como por el uso de un hashtag. Entonces, el objetivo del proyecto es poder clasificar que ciudades son las que más imágenes asociadas a su ubicación

La API de Twitter nos permite acceder a ella de forma más simple que la de Instagram, es por eso que me he decantado por esta red social. A continuación, se muestran algunos datos a los que podemos acceder [1]:

- __Tweets__: búsqueda, publicación, filtrado, etc.
- Anuncios: gestión de campañas, análisis, etc.
- __Contenido multimedia__: subir y acceder a fotos, videos, GIF animados, etc.
- Tendencias: _trending topics_.
- __Geo__: información sobre lugares conocidos, lugares cerca de una ubicación, etc.

## Arquitectura software

Actualmente, las arquitecturas software modernas buscan la consistencia en la velocidad de respuesta al usuario. Sin embargo, en el mercado existen muchos tipos de arquitecturas, es por ello que a veces se hace difícil concretar qué arquitectura se va a utilizar [2]:

- __Arquitectura en capas__: arquitectura cliente-servidor, creando 3 o más capas, normalmente se suelen incluir la capa de presentación, la de aplicación, la de lógica de negocio y la de acceso a datos. El problema principal es que solo permite escalado dentro de cada una de las capas, siendo al final alguna de ellas un cuello de botella.
- __Arquitectura dirigida por eventos__: tiene una cola de eventos que se originan en el usuario, pero también de una parte a otra de la arquitectura. Es difícil de testear y su desarrollo es más complicado que la anterior.
- __Arquitectura microkernel__: arquitectura casi monolítica, con un núcleo central al que se pueden añadir funcionalidades mediante plugins, siendo su problema principal la escalabilidad, ya que el núcleo puede representar un cuello de botella.
- __Arquitectura basada en microservicios__: arquitectura muy popular hoy en día, se caracteriza por poder usar unidades que se van a desplegar de forma independiente y por poder usar tecnologías subyacentes que van desde la virtualización completa en la nube hasta el uso de contenedores Docker en una sola máquina virtual.
__Arquitectura basada en espacios__: arquitectura antigua, de la década de los 90.

Entonces, resulta bastante claro que de todas las comentadas anteriormente vayamos a hacer uso de la __arquitectura basada en microservicios__, ya que es la que más actual y la que menos problemas presenta, además de que nos permite tener diferentes servicios trabajando de forma totalmente independiente unos de otros.

### Microservicios a desarrollar

[imagen icono twitter] + [imagen icono python]

Para realizar la arquitectura se va a hacer uso del lenguaje [Python](https://www.python.org), y para el desarrollo de los microservicios se puede usar cualquier microframework web para Python, en este caso existe la posibilidad de usar [Django](https://www.djangoproject.com) (más complejo o pensado para  que crezca) o [Flask](http://flask.pocoo.org) (más sencillo). Es por ello, que al ser la primera vez para mí, me he decantado por Flask.

Los microservicios previstos a desarrollar son los siguientes:

[imagen de la estructura]

1. __Consultar API de Twitter__: en este microservicio solo nos vamos a centrar en acceder, consultar y bajarnos información de la API, información obtenida en un [JSON](https://www.json.org).
2. __Procesar información__: en este microservicio vamos a quedarnos con los datos referentes a las imágenes que tienen localización o el hashtag de esa localización, en un JSON.
3. __Almacenar información__: en este microservicio nos vamos a centrar en crear una estructura para los datos que hemos realizado, usando principalmente una BD como (MongoDB)[https://www.mongodb.com/es].
4. __Mostrar información__: en este microservicio solo nos interesa mostrar la información relevante de alguna manera específica.

Además, necesitamos un sistema de centralización de [__logs__](https://www.elastic.co/products/logstash), al cual todos deben comunicarse.

### Comunicación entre los microservicios

La comunicación entre servicios será realizada por _brokers_, en concreto con (RabbitMQ)[https://www.rabbitmq.com], que es un sistema de manejo de colas.

### Bibliotecas de Python para la API de Twitter

Python cuenta muchas bibliotecas desarrolladas para la API de Twitter. Sin embargo, al no haber usado nunca ninguna me es dífil elegir que biblioteca es la mejor. Es por ello, que voy hacer uso de (tweepy)[https://github.com/tweepy/tweepy] ya que he oído hablar de ella bastante bien. De todas maneras, existen otras librerías cómo (twython)[https://github.com/ryanmcgrath/twython], (python-twitter)[https://github.com/bear/python-twitter] o (TwitterAPI)[https://github.com/geduldig/TwitterAPI]

### Tests en Python

Para testear en Python [3], podré usar algunas de las librerías que me permiten implementar pruebas unitarias en dicho lenguaje como (unittest)[https://docs.python.org/3.5/library/unittest.html], (doctest)[https://docs.python.org/3.5/library/doctest.html] o (pytest)[https://docs.pytest.org/en/latest/] [4].

Además para testear en Python, también tengo la posibilidad de hacer uso de (Travis CL)[https://www.travis-ci.org], que es un sistema distribuido de generación e integración continua libre, que me permite conectar mi repositorio de Github y testear después de cada push que haga [5] [6].

### Despliegue en la nube

Los microservicios serán desplegados en la nube, para el despliege del proyecto se puede utilizar una maquina virtual en Azure.

#### Uso de PaaS

Cuando se quiere desplegar una aplicación sobre una infraestructura ya definida y que no va a cambiar se necesita un _Platform as a Service_ o PaaS. Entre los posibles servicios que hay vamos a escoger entre (Heroku)[https://www.heroku.com] o (OpenShift)[https://www.openshift.com].

## Licencia

Proyecto bajo licencia (GNU GLP V3)[https://github.com/Gecofer/proyecto-CC/blob/master/LICENSE].

## Referencias

[1] https://stackabuse.com/accessing-the-twitter-api-with-python/
[2] https://github.com/JJ/CC/blob/master/documentos/temas/Arquitecturas_para_la_nube.md
[3] https://github.com/JJ/tests-python
[4] https://recursospython.com/guias-y-manuales/unit-testing-doc-testing/
[5] https://www.smartfile.com/blog/testing-python-with-travis-ci/
[6] https://github.com/softwaresaved/build_and_test_examples

## Enlaces de Interés

- [Publics APIs](https://github.com/toddmotto/public-apis#books)


Nota: Se debe tener en cuenta que a lo largo del desarrollo de la aplicación, se podrá modificar la documentación o añadir nuevas funcionalidades.
