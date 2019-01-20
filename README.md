# Análisis de tendencias (geolocalizadas) en Twitter

Proyecto de la asignatura Cloud Computing para el curso 2018/2019 del Máster en Ingeniería Informática, realizado por Gema Correa Fernández. Pincha [aquí](https://gecofer.github.io/proyecto-CC/) para acceder al enlace de la documentación.

**Tabla de Contenidos**

- [Novedades](#id0)
- [Descripción del proyecto](#id1)
- [Descripción de arquitecturas software](#id2)
  - [Arquitectura seleccionada](#id3)
- [Descripción de los microservicios a desarrollar](#id4)
  - [Bibliotecas de Python para la API de Twitter](#id6)
- [Descipción de los tests en Python (código sin test código roto)](#id7)
- [Descripción del despliegue](#id8)
  - [Despliegue en PaaS](#id9)
  - [Despliegue de la infraestructura en máquina virtual local](#id10)
- [Orquestación de máquinas virtuales](#id20)
  - [Pasos para probarlo](#id21)
  - [Comprobaciones del hito 5](#id22)
- [Enlaces de Interés](#id15)
- [Licencia](#id16)

<!----

  - [Comunicación entre los microservicios](#id5)


- [Descripción del despliegue](#id8)
  - [Despliegue en PaaS](#id9)
  - [Despliegue de la infraestructura en máquina virtual local:](#id10) en [Vagrant](#id11) y en [Ansible](#id12)
- [Automatización de tareas en la nube](#id13)


MV2: 40.89.158.208


Despliegue: https://glacial-castle-84194.herokuapp.com

MV: 23.97.225.1

(http://23.97.225.1)[http://23.97.225.1]
--->

## Novedades <a name="id0"></a>

<!----
- Pincha [aquí](https://github.com/Gecofer/ejercicios-CC/tree/master/hito4/Seminarios/Chef) para ver el resumen realizado sobre el seminario de Chef.
- Pincha [aquí](https://github.com/Gecofer/ejercicios-CC/tree/master/hito4/Seminarios/Nube%20desde%20linea%20de%20ordenes) para ver el resumen realizado sobre el seminario de la nube desde línea de órdenes.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/tree/master/provision) para acceder a la documentación trasladada del hito 3.
- Pincha [aquí](#id13) para localizar el nuevo apartado de **automatización de tareas en la nube**, correspondiente al hito 4 (se explica porque se hace uso de la CLI de Azure).
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/automatizar-creacion-mv.md#id0) para ver los pasos para la creación de una instancia en la nube.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/automatizar-creacion-mv.md#id3) para aprender a instalar la CLI de Azure e iniciar sesión y autenticarse.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/automatizar-creacion-mv.md#id5) para aprender a listar imágenes de máquinas virtuales con la CLI de Azure.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/eleccion-mv-centro-datos.md#id0) para ver la justificación de la elección de la imagen del sistema operativo.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/eleccion-mv-centro-datos.md#id11) para ver la justificación de la elección del tamaño de la imagen de la máquina virtual.
- Pincha [aquí](https://www.danielstechblog.io/azure-vm-sizes/) para ver que tamaños de imágenes están disponibles en cada ubicación/región.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/eleccion-mv-centro-datos.md#id2) para ver la justificación de la elección del centro de datos.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/avance_proyecto.md) para acceder a los avances realizados en el hito 4.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/acopio.sh) para ver el script de aprovisionamiento, [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/acopio.md) para ver la documentación del mismo y [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/salida-acopio.txt) para ver su salida.
- Pincha [aquí](https://github.com/Gecofer/ejercicios-CC/blob/master/hito4/objetivosHito4.md) para más información acerca de como se ha redirigido el puerto 5000 usado por Flask al puerto 80.


- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/errores_proyecto.md) para acceder a los errores solucionados a lo largo del hito 3.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/avance_proyecto.md) para acceder a los avances realizados en el hito 3.
- Pincha [aquí](https://github.com/Gecofer/ejercicios-CC) para acceder a los ejercicios de la asignatura (resúmenes de charlas, ejercicios, enlaces de interés...).
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/tree/master/provision) para ver el despliegue realizado en una máquina local y en Azure.
- Pincha [aquí](#id14) para ver las comprobaciones de provisionamiento del hito 3 entre [@jmv74211](https://github.com/jmv74211/) y [@gecofer](https://github.com/Gecofer).
- Pincha [aquí](https://github.com/Gecofer/ejercicios-CC/blob/master/hito3/Charla%20logs/logs.md) para ver el resumen realizado de la charla impartida sobre `logs`.
- Pincha [aquí](https://github.com/Gecofer/ejercicios-CC/blob/master/hito3/pyenv.md) para ver como se ha puesto un _environment_ a la carpeta del proyecto de la asignatura.
- Pincha [aquí](https://github.com/Gecofer/proyecto-CC/tree/master/provision/Azure#id4) para más información acerca de como se ha redirigido el puerto 5000 usado por Flask al puerto 80.
--->

## Descripción del proyecto <a name="id1"></a>

Twitter junto con Instagram son dos de las plataformas sociales más usadas actualmente, por eso mismo, miles de usuarios comparten todo tipo de información en ellas. Este tipo de comportamientos benefician a las empresas dándoles potestad en la obtención de información muy valiosa, cómo por ejemplo ver qué tendencias o _trending topics_ son los más comentados o qué ciudades son las más comentadas en la red. En este caso, yo me voy a centrar en la obtención de datos geolocalizados, es decir,  en la extracción de _trending topics_ o tendencias de los usuarios en Twitter para una región determinada. Para así, poder clasificar las tendencias y establecer la tendencia mayoritaria para una region determinada.


## Descripción de arquitecturas software <a name="id2"></a>

Actualmente, las arquitecturas software modernas buscan la consistencia en la velocidad de respuesta al usuario. Sin embargo, en el mercado existen muchos tipos de arquitecturas, es por ello que a veces se hace difícil concretar qué arquitectura se va a utilizar [[2][2]]:

- __Arquitectura en capas__.
- __Arquitectura dirigida por eventos__.
- __Arquitectura microkernel__.
- __Arquitectura basada en microservicios__.
- __Arquitectura basada en espacios__.

_**Pincha [aquí](https://gecofer.github.io/proyecto-CC/#id2) para saber más acerca de las arquitecturas anteriores.**_

### Arquitectura seleccionada <a name="id3"></a>

Entonces, resulta bastante claro que de todas las arquitecturas comentadas anteriormente vayamos a hacer uso de la __arquitectura basada en microservicios__, ya que es la que más actual y la que menos problemas presenta, además de que nos permite tener diferentes servicios trabajando de forma totalmente independiente unos de otros.

## Descripción de los microservicios a desarrollar <a name="id4"></a>

<p align="center">
  <img width="210" height="90" src="docs/images/twitter+python.png">
</p>

Para realizar la arquitectura se va a hacer uso del lenguaje [Python](https://www.python.org), y para el desarrollo de los microservicios se puede usar cualquier microframework web para Python, en este caso existe la posibilidad de usar [Django](https://www.djangoproject.com) (más complejo o pensado para un proyecto de grandes dimensiones o que crezca) o [Flask](http://flask.pocoo.org) (más sencillo). Es por ello, que tras haber buscado documentación, hablado con usuarios de ambos microframework y ser la primera vez que uso este tipo de tecnología/herramienta, me he decantado por Flask. Los microservicios previstos a desarrollar son los siguientes:

1. __Consultar API de Twitter__: en este microservicio solo nos vamos a centrar en acceder, consultar y bajarnos información de la API, información obtenida en un [JSON](https://www.json.org).
2. __Procesar información__: en este microservicio vamos a quedarnos con los datos referentes a las tendencias según su localización, en un JSON: [`API.trends_place(id[, exclude])`](http://docs.tweepy.org/en/v3.5.0/api.html).
3. __Almacenar información__: en este microservicio nos vamos a centrar en crear una estructura para los datos que hemos realizado, usando principalmente una BD como [MYSQL](https://www.mysql.com).
4. __Mostrar información__: en este microservicio solo nos interesa mostrar la información relevante de alguna manera específica.
5. Además, necesitamos un sistema de centralización de [__logs__](https://www.elastic.co/products/logstash), al cual todos deben comunicarse.

<p align="center">
  <img width="460" height="350" src="docs/images/estructura_microservicios.png">
</p>

<!----
### Comunicación entre los microservicios <a name="id5"></a>


La comunicación entre servicios será realizada por _brokers_, en concreto con [RabbitMQ](https://www.rabbitmq.com), que es un sistema de manejo de colas.
--->


### Bibliotecas de Python para la API de Twitter <a name="id6"></a>

Actualmente, la API de Twitter nos permite acceder a todo tipo de información de forma más simple que la de Instagram, es por eso que me he decantado por esta red social. A continuación, se muestran algunos datos a los que podemos acceder [[1][1]]:

- __Tweets__: búsqueda, publicación, filtrado, etc.
- __Anuncios__: gestión de campañas, análisis, etc.
- __Contenido multimedia__: subir y acceder a fotos, vídeos, GIF animados, etc.
- __Tendencias__: _trending topics_.
- __Geo__: información sobre lugares conocidos, lugares cerca de una ubicación, etc.

Python cuenta muchas bibliotecas desarrolladas para la API de Twitter. Sin embargo, al no haber usado nunca ninguna me es dífil elegir que biblioteca es la mejor. Es por ello, que voy hacer uso de [tweepy](https://github.com/tweepy/tweepy) ya que he oído hablar de ella bastante bien y tiene bastante documetación en la web. De todas maneras, existen otras librerías cómo [twython](https://github.com/ryanmcgrath/twython), [python-twitter](https://github.com/bear/python-twitter) o [TwitterAPI](https://github.com/geduldig/TwitterAPI).

_**Pincha [aquí](https://github.com/Gecofer/proyecto-CC/tree/master/data), para más información acerca de la extracción de datos de Twitter realizada para el proyecto**_


## Descipción de los tests en Python (código sin test código roto) <a name="id7"></a>

Para testear en Python [[3][3]], puedo usar algunas de las librerías que me permiten implementar pruebas unitarias en dicho lenguaje como [unittest](https://docs.python.org/3.5/library/unittest.html), [doctest](https://docs.python.org/3.5/library/doctest.html) o [pytest](https://docs.pytest.org/en/latest/) [[4][4]]. En este caso yo voy hacer uso de la biblioteca [unittest](https://docs.python.org/3.5/library/unittest.html), ya que nos ofrece toda la potencia del lenguaje para probar nuestros programas, lo que significa que ayuda a determinar rápidamente el impacto de cualquier modificación en el resto del código.

Para realizar la configuración de los tests correctamente, voy hacer uso de [Travis CL](https://www.travis-ci.org), que es un sistema distribuido de generación e integración continua libre, que me permite conectar mi repositorio de Github y testear después de cada push que haga [[5][5]] [[6][6]].

_**Pincha [aquí](https://gecofer.github.io/proyecto-CC/#id6), para saber más información sobre los tests.**_

## Descripción del despliegue <a name="id8"></a>

### Despliegue en PaaS <a name="id9"></a>

Cuando se quiere desplegar una aplicación sobre una infraestructura ya definida y que no va a cambiar se necesita un _Platform as a Service_ o PaaS. Entre los posibles servicios que hay [Heroku](https://www.heroku.com) o [OpenShift](https://www.openshift.com), vamos a escoger [Heroku](https://www.heroku.com), ya que es un servicio fiable, gratuito, ofrece muchas opciones a la hora de elegir el lenguaje y permite integrar Github con Travis.

<!----
Despliegue: https://glacial-castle-84194.herokuapp.com
--->
_**Pincha [aquí](https://gecofer.github.io/proyecto-CC/#id9), para saber más información sobre el despliegue en PaaS.**_

### Despliegue de la infraestructura en máquina virtual local <a name="id10"></a>

Para el despliegue de la aplicación en una máquina virtual local, se ha hecho uso de Ansible junto con Vagrant. Previamente a la realización de un `clone` a mi repositorio, se debe instalar [Ansible](https://github.com/Gecofer/proyecto-CC/tree/master/provision),  [Vagrant](https://github.com/Gecofer/proyecto-CC/tree/master/provision/vagrant-ubuntu) y [VirtualBox](https://www.virtualbox.org), herramientas necesarias para ejecutar la aplicación. Una vez realizados estos procesos, debemos dirigirnos al directorio `provision > vagrant_ubuntu` y ejecutar la sentencia `vagrant up`, la cual creará una máquina virtual en VirtualBox y ejecutará el _playbook_ con lo indispensable para el despliegue.

<!----

#### Vagrant <a name="id11"></a>

Se ha utilizado la herramienta Vagrant para generar entornos de desarrollo reproducibles y compartibles de forma muy sencilla, ya que crea y configura máquinas virtuales a partir de simples ficheros de configuración. El fichero donde se describe la infraestructura se llama `Vagrantfile` y es utilizado para el despliegue ([enlace](https://github.com/Gecofer/proyecto-CC/blob/master/provision/vagrant-ubuntu/Vagrantfile)).

_**Pincha [aquí](https://github.com/Gecofer/proyecto-CC/tree/master/provision/vagrant-ubuntu), para saber más información sobre el despliegue en máquina virtual local con Vagrant.**_

#### Ansible <a name="id12"></a>

Para el provisionamiento se ha hecho uso de Ansible (versión 2.7.2)
Como software para automatizar el proceso de aprovisionamiento se ha utilizado Ansible, creando previamente los siguientes ficheros:

- [**ansible.cfg**](https://github.com/Gecofer/proyecto-CC/blob/master/provision/vagrant-ubuntu/ansible.cfg): fichero de configuración básica, que básicamente le dice a Ansible que tiene que mirar en el fichero ansible_hosts.
- [**ansible_hosts**](https://github.com/Gecofer/proyecto-CC/blob/master/provision/vagrant-ubuntu/ansible_hosts): fichero para definir una serie de requerimentos (nombre de la máquina, puerto SSH para acceder a la máquina virtua, host).
- [**ansible_playbook.yml**](https://github.com/Gecofer/proyecto-CC/blob/master/provision/vagrant-ubuntu/ansible_playbook.yml): fichero para definir las intrucciones a ejecutar (python, git, pip, flask, clonar repositorio).

_**Pincha [aquí](https://github.com/Gecofer/proyecto-CC/tree/master/provision), para saber más información sobre la gestión de configuraciones con Ansible.**_

_**Pincha [aquí](https://github.com/Gecofer/proyecto-CC/tree/master/provision/Azure), para saber más información sobre el despliegue en Azure.**_
--->
<!----
Si no se utiliza Vagrant, también se puede realizar el provisionamiento utilizando órdenes de ansible, es decir, haciendo uso de la orden `ansible-playbook ansible_playbook.yml`.


### Despliegue de la infraestructura en Azure  <a name="id13"></a>

Se ha creado una máquina virtual en Azure con Ubuntu 14.04 LTS, la misma usada para el despliegue en la máquina virtua local. Para lanzar la aplicación, debemos conectar a la mv `ssh gemaAzure@23.97.225.1` y ejecutar el provisionamiento que con todos los módulos necesarios se uso de `ansible-playbook -i ansible_hosts -b ansible_playbook.yml`.

![](/docs/images/azure7.png)

![](/docs/images/azure3.png)

Lanzamos nuestra aplicación con [_gunicorn_](https://gunicorn.org) y efectivamente comprobamos que podemos aceder:

![](/docs/images/azure5.png)

![](/docs/images/azure8.png)

La dirección IP: 23.97.225.1

MV: [http://23.97.225.1](http://23.97.225.1)
--->
<!----
*__Pincha [aquí](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/correcci%C3%B3n_a_%40Gecofer.md) para ver la comprobación de [@jmv74211](https://github.com/jmv74211/) al aprovisionamiento de [@gecofer](https://github.com/Gecofer).__*

__*Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/corrección_a_%40jmv74211.md#comprobación-de-la-aplicación-en-azure) para ver la comprobación de [@gecofer](https://github.com/Gecofer) al aprovisionamiento de [@jmv74211](https://github.com/jmv74211/).*__


## Automatización de tareas en la nube <a name="id13"></a>

El objetivo de las plataformas de virtualización es, eventualmente, crear y gestionar una máquina virtual que funcione de forma aislada del resto del sistema y que permita trabajar con sistemas virtualizados de forma flexible, escalable y adaptada a cualquier objetivo. Para ello, usaremos los clientes de línea de órdenes de los servicios en la nube para crear instancias de máquinas virtuales y otros recursos necesarios para las mismas. Estas instancias, posteriormente, se provisionarán y se instalará en ella la aplicación que se ha venido usando hasta ahora.

1. En este caso vamos hacer uso de la **CLI de Azure**, para ello primero deberemos instalarla, y una vez instalada iniciar sesión y autenticarse en el mismo, además de unos pequeños comandos para ver el listado de imágenes de máquinas virtuales disponibles (_**pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/automatizar-creacion-mv.md) para ver la documentación**_).

  Se va hacer uso del CLI de Azure, debido a que dispongo de más conocimientos en su manejo, al ser, personalmente más sencillo. Debido a que pedí patrocinio con Amazon Cloud Services mediante la cuenta de la UGR hace unas semanas y aún sigo esperando la respuesta, es por eso que se ha descartado su uso en este hito. Además, hace menos de una semana se nos proporcionó acceso al patrocinio de Google Cloud, sin embargo, no se ha podido llevar a cabo principalmente por un motivo: no he tenido tiempo de llevarlo a cabo debido a que me ha resultado más complejo de primeras, pero espero poder usarlo para el siguiente hito.

2. Una vez que podemos crear máquinas virtuales desde la línea de comandos, vamos a razonar la justificación de la **elección de la imagen** del sistema operativo (_**pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/eleccion-mv-centro-datos.md#id0) para ver dicha justificación**_). En nuestro caso, hemos seleccionado el sistema Ubuntu Server 18.04 LTS.

3. Una vez escogido el sistema operativo, pasamos a la elección del tamaño de la imagen para dicha máquina virtual (_**pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/eleccion-mv-centro-datos.md#id11) para ver dicha justificación**_).

4. Una vez escogido el sistema operativo, se va a justificar la **elección del centro de datos** en el cual se creará la máquina virtual (_**pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/eleccion-mv-centro-datos.md#id1) para ver dicha justificación**_). En este caso, se ha hecho uso del centro de datos del centro de Francia.

5. Por último, ya solo nos hace falta crear el script de aprovisionamiento, para eso pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/acopio.sh) para ver el código, [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/acopio.md) para ver la documentación del mismo y [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/salida-acopio.txt) para ver su salida.

--->

## Orquestación de máquinas virtuales <a name="id20"></a>

Se va a usar `Vagrant` para provisionar una o preferiblemente varias máquinas virtuales usando un proveedor de servicios cloud, en este caso se ha usado Azure.

### Pasos para probarlo <a name="id22"></a>

1. Clonar mi repositorio.
2. Acceder a la carpeta orquestación (`cd orquestacion/`) y ejecutar `vagrant up --no-parallel —provider=azure`.
3. Cuando se terminen de crear y provisiona ambas máquinas, abrir las dos con SSH:

  ~~~
  # Para la máquina principal
  $ ssh vagrant@mvprincipalcc.francecentral.cloudapp.azure.com

  # Para la máquina con la base de datos
  $ ssh vagrant@mvbasedatoscc.francecentral.cloudapp.azure.com
  ~~~

4. Dentro de la máquina principal, se accede a la carpeta proyecto (`cd proyecto/`) y se lanza la aplicación en el puerto 80 con (`sudo gunicorn -b :80 main:app`).

5. Accedemos al navegador con la IP pública de la máquina principal (http://ip_publica_maquina_principal:80/status) y obtenemos el _status ok_ (mirar IP en Azure).

6. Accedemos al navegador con la IP pública de la máquina principal (http://ip_publica_maquina_principal:80/BD) y visualizamos la interfaz web, la cual esta conectada con la base de datos.

### Comprobaciones del hito 5 <a name="id22"></a>

- Comprobación de [@jmv74211](https://github.com/jmv74211) al aprovisionamiento de [@gecofer](https://github.com/Gecofer) disponible en este [enlace](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/correcci%C3%B3n_a_%40Gecofer_hito5.md).

- Comprobación de [@gecofer](https://github.com/Gecofer) al aprovisionamiento de [@jmv74211](https://github.com/jmv74211) disponible en este [enlace](https://github.com/Gecofer/Proyecto-cloud-computing/blob/master/docs/hitos/comprobacion_hito5_de_%40Gecofer.md).

- Comprobación de [@luiisgallego](https://github.com/luiisgallego/MII_CC_1819) al aprovisionamiento de [@gecofer](https://github.com/Gecofer) disponible en este [enlace](https://github.com/Gecofer/proyecto-CC/blob/master/docs/comprobacionAprovision.md).

- Comprobación de [@gecofer](https://github.com/Gecofer) al aprovisionamiento de [@luiisgallego](https://github.com/luiisgallego/MII_CC_1819) disponible en este [enlace](https://github.com/luiisgallego/MII_CC_1819/blob/master/docs/comprobacionHito5.md).


## Enlaces de Interés <a name="id15"></a>

- [Publics APIs](https://github.com/toddmotto/public-apis#books)


## Licencia <a name="id16"></a>

Proyecto bajo licencia [GNU GLP V3](https://github.com/Gecofer/proyecto-CC/blob/master/LICENSE).


[1]: https://stackabuse.com/accessing-the-twitter-api-with-python/
[2]: https://github.com/JJ/CC/blob/master/documentos/temas/Arquitecturas_para_la_nube.md
[3]: https://github.com/JJ/tests-python
[4]: https://recursospython.com/guias-y-manuales/unit-testing-doc-testing/
[5]: https://www.smartfile.com/blog/testing-python-with-travis-ci/
[6]: https://github.com/softwaresaved/build_and_test_examples



*__Nota__: Se debe tener en cuenta que la realización de un proceso de desarrollo conlleva modificaciones en el futuro, pudiendo modificar la documentación o añadiendo nuevas funcionalidades.*

---
