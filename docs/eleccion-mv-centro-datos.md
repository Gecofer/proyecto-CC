# Creación de la misma máquina virtual en distintos centros de datos <a name="id6"></a>

**Tabla de Contenidos**
- [Elección del sistema operativo](#id0)
  - [Entonces, ¿CentOS o Ubuntu?](#id1)
- [Elección del centro de datos](#id2)
  - [Crear máquina virtual con Ubuntu Server 18.04 LTS en el centro de datos del centro de Francia](#id3)
    - [Medición de prestaciones con httperf](#id4)
    - [Medición de prestaciones con ab](#id5)
  - [Crear máquina virtual con Ubuntu Server 18.04 LTS en el centro de datos del sur de Francia](#id6)
  - [Crear máquina virtual con Ubuntu Server 18.04 LTS en el centro de datos del oeste de Reino Unido](#id7)
    - [Medición de prestaciones con httperf](#id8)
    - [Medición de prestaciones con ab](#id9)
  - [Crear máquina virtual con Ubuntu Server 18.04 LTS en el centro de datos del norte de Europa](#id10)
    - [Medición de prestaciones con httperf](#id11)
    - [Medición de prestaciones con ab](#id12)
  - [Tabla comparativa de mediciones con httperf](#id13)
  - [Tabla comparativa de mediciones con ab](#id14)

## Elección del sistema operativo <a name="id0"></a>

Antes de empezar con la creación de las máquinas virtuales en distintos centros de datos, vamos a detenernos un momento y pensar que tipo de SO nos conviene usar para nuestro proyecto, en el cual se hace uso de [Python](https://www.python.org) y de [Flask](http://flask.pocoo.org), indistintamente.

La comunidad de código abierto provee Linux al mundo Python como un sistema operativo libre y sólido para ejecutar dichas aplicaciones. Es por eso, que los únicos sistemas operativos recomendados para la producción de implementaciones en Python son Linux y FreeBSD, es decir, las versiones de Ubuntu Long Term Support (LTS), Red Hat Enterprise Linux y CentOS son las opciones viables [[2][2]]. Veamos en que difieren cada una de ellas:

- **Ubuntu Long Term Support (LTS)**: son las versiones recomendadas para las implementaciones, ya que reciben cinco años de actualizaciones posteriores a su publicación. Además, de que cada dos años, Canonical crea una nueva versión de LTS, lo que permite una fácil ruta de actualización, así como flexibilidad para saltarse cualquier otra versión de LTS si es necesario. La última versión de Ubuntu LTS es 18.04 Bionic Beaver, en la cual se incluye Python 3.6 como su versión predeterminada de Python, que es una actualización importante en comparación con la 2.7 en Ubuntu 14.04 LTS y una sólida mejora sobre Python 3.5 incluida en Ubuntu 16.04 LTS. Veamos las versiones de Python de las últimas versiones LTS:

  - Ubuntu 14.04 LTS trae por defecto la versión de Python 2.7.6 y 3.4.0 [[2][2]]
  - Ubuntu 16.04 LTS trae por defecto la versión de Python 2.7 y 3.5 [[3][3]]
  - Ubuntu 18.04 LTS trae por defecto la versión de Python 2.7 y 3.6 [[4][4]]


- **Red Hat Enterprise Linux (RHEL)** y **Community ENTerprise Operating System (CentOS)** son la misma distribución. La principal diferencia entre los dos, reside en que CentOS es un derivado libre de RHEL de código abierto y con licencias gratuitas. RHEL y CentOS utilizan un gestor de paquetes y una interfaz de línea de comandos diferentes de las distribuciones de Linux basadas en Debian: RPM Package Manager (RPM) y el Yellowdog Updater, Modified (YUM).

### Entonces, ¿CentOS o Ubuntu? <a name="id1"></a>

- [CentOS vs Ubuntu: ¿Cuál elegir para tu servidor web?](https://www.hostinger.es/tutoriales/centos-vs-ubuntu-elegir-servidor-web/#gref)
- [What is best production server for Flask apps: Ubuntu or CentOS?](https://www.quora.com/What-is-best-production-server-for-Flask-apps-Ubuntu-or-CentOS)

| Ubuntu | CentOS |
|-------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| Basado en Debian | Basado en RHEL |
| Actualizado frecuentemente | Actualizado con poca frecuencia |
| No admite cPanel (tiene alternativas) | Admite cPanel/WHM |
| Comunidad más grande de usuarios y desarrolladores  | Comunidad más pequeña de usuarios y desarrolladores |
| Mayor cantidad de ayuda disponible en forma de tutoriales y guías gratuitas | Menor cantidad de ayuda disponible |
| Más fácil de aprender para los principiantes que han usado el escritorio de Ubuntu en el pasado | Más difícil de aprender para los principiantes ya que no hay muchas distribuciones de escritorio famosas lanzadas por RHEL |
| Los paquetes .deb se instalan usando el administrador de paquetes apt-get | Los paquetes .rpm se instalan usando el administrador de paquetes yum |

Por otro lado, podemos considerar diferencias en cuanto a velocidad, sin embargo, casi no hay al tratarse de Ubuntu contra CentOS. Ya que el hardware físico en el que se ejecuta la aplicación será más importante en términos de velocidad que el sistema operativo. Además, según varias encuestas, Ubuntu es el sistema operativo más popular del mundo para ejecutar servidores web, funcionando en un 34% de todos los servidores web [[10][10]].

Por otra parte, algunos usuarios sugieren que han tenido problemas con YUM y RPM para la instalación de ciertos paquetes en RHEL, en donde dichos problemas se han solucionado migrando a Ubuntu, ya que los repositorios de código fuente _apt_ resuelven muchas dependencias. Además, se aconseja que Ubuntu es muy adecuado para trabajar con contenedores (_dockers_) [[11][11]].

Es por ello que voy hacer uso de una versión LTS de Ubuntu para mi proyecto, debido a la estabilidad, y la instalación predefinida de Python tanto para la versión 2 como 3. Ya que CentOS sólo se actualiza con versiones de puntos que pueden causar problemas con algunos módulos de Python, y es necesario para los servicios del sistema, por lo que el procedimiento estándar es instalar una segunda versión en _/opt_ para usar en aplicaciones [[5][5]]. Además, en el hito anterior, se llevó a cabo el provisionamiento tanto en Ubuntu como en CentOS, lo que sirvió para detectar fallos en cuanto a la instalación de los requerimientos del proyecto. Además, en el siguiente [enlace](https://www.quora.com/What-is-best-production-server-for-Flask-apps-Ubuntu-or-CentOS) se nos recomienda que usemos Ubuntu LTS en aplicaciones a usar Flask.

Sin embargo, una vez elegido el Ubuntu Server LTS como sistema operativo, vamos a ver que versión escoger de dicho SO. A continuación, se ven los ciclos de vida de las versiones de Ubuntu [[6][6]]:

<p align="center">
  <img width="550" height="260" src="images/hito 4/ciclo-ubuntu.png">
</p>

Como podemos comprobar, la versión 14.04 LTS termina su mantenimiento en 2019, esto puede suponer un problema si la asignatura se alarga durante ese año. Es por eso que descartamos la versión 14.04. Por otro lado, tanto las versiones 16.04 como 18.04, disponen de más años de mantenimiento. Sin embargo, el tiempo de soporte de Ubuntu 18.04 se ha aumentado de 5 a 10 años, punto a favor sobre esa versión [[7][7]]. Además, la última versión de Python estable es la 3.6 y dicha versión viene instalada por defecto en la 18.04 LTS y es la versión que estoy usando en mi proyecto.

**Por tanto, podemos confirmar que el mejor SO para nuestro proyecto es la versión de Ubuntu Server 18.04 LTS.**


## Elección del centro de datos <a name="id2"></a>

Para escoger el centro de datos, en el cual desplegar nuestra aplicación, vamos a obtener las mediciones de velocidad de las máquinas virtuales creadas con las mismas características (Ubuntu Server 18.04 LTS), haciendo uso de herramientas como `ab` o `httperf`. Lo primero que tenemos que saber son los [centros de datos de los que dispone Azure](https://azure.microsoft.com/es-es/global-infrastructure/regions/) [[8][8]].

~~~
# Listar las regiones admitidas para la suscripción actual
$ az account list-locations
~~~

<p align="center">
  <img width="650" height="450" src="images/hito 4/regiones-azure.png">
</p>

_**Pincha [aquí](https://github.com/Gecofer/proyecto-CC/blob/master/docs/salida-centros-datos.txt) para ver la lista completa.**_

Es lógico, que el centro de datos a usar sea cercano a nuestra ubicación actual, con el fin de obtener unas buenas prestaciones. Es por ello, que nos quedamos con los centros de datos disponibles en Europa:

- **Centro de Francia** (_francecentral_), ubicado en latitud 46.3772 y longitud 2.3730
- **Sur de Francia** (_francesouth_), ubicado en latitud 43.8345 y longitud 2.1972
- **Sur de Reino Unido** (_uksouth_), ubicado en latitud 50.941 y longitud -0.799
- **Oeste de Reino Unido** (_ukwest_), ubicado en latitud 53.427 y longitud -3.084
- **Norte de Europa** (_northeurope_), ubicado en latitud 53.3478 y longitud -6.2597
- **Oeste de Europa** (_westeurope_), ubicado en latitud 52.3667 y longitud 4.9

Debido a que la creación de recursos como de máquinas virtuales consumen dinero en Azure, se ha optado por hacer una comparación entre las tres localizaciones más cercanas a Granada (latitud: 37.1886273, longitud: -3.5907775) [[9][9]].

- Distancia de Granada al Centro de Francia: 1135.36 km
- Distancia de Granada al Sur de Francia: 886.62 km
- Distancia de Granada al Sur de Reino Unido: 1546.57 km
- Distancia de Granada al Oeste de Reino Unido: 1807.79
- Distancia de Granada al Norte de Europa: 1810.33 km
- Distancia de Granada al Oeste de Europa: 1814.68 km

Por tanto, se van a comprobar los centros de datos del **Centro de Francia**, **Sur de Francia** y **Sur de Reino Unido**, para nuestra aplicación.

### Crear máquina virtual con Ubuntu Server 18.04 LTS en el centro de datos del centro de Francia <a name="id3"></a>

Antes de la creación de la máquina virtual, vamos a listar las disponibles en dicha región que contienen como sistema operativo Ubuntu Server.

~~~
# Listar mv con localización en el centro de Francia con Ubuntu Server
$ az vm image list-skus --location francecentral --publisher Canonical --offer UbuntuServer --output table
~~~

<p align="center">
  <img width="650" height="230" src="images/hito 4/lista-Ubuntu-francecentral.png">
</p>

A continuación, se listan las versiones de Ubuntu Server 18.04 LTS:

~~~
# Listar mv con localización en el centro de Francia con Ubuntu Server 18.04 LTS
$ az vm image list --location francecentral --publisher Canonical --offer UbuntuServer --sku 18.04-LTS --all --output table
~~~

<p align="center">
  <img width="650" height="230" src="images/hito 4/lista-Ubuntu1804-francecentral.png">
</p>

Por último, se visualiza la información sobre la última máquina de dicha versión:

~~~
# Visualizar la información sobre una máquina virtual en concreto
$ az vm image show --location francecentral --urn Canonical:UbuntuServer:18.04-LTS:18.04.201812060
~~~

<p align="center">
  <img width="650" height="160" src="images/hito 4/informacion-Ubuntu-concreta.png">
</p>

Una vez, que tenemos decidida nuestra máquina virtual, vamos a proceder a crearla. Para ello, lo primero que haremos será crear el grupo de recursos para indicar el centro de datos en el que se va a alojar, en este caso en el centro de Francia.

~~~
# Crear el grupo de recursos
$ az group create --name myResourceGroup-francecentral --location francecentral
~~~

A continuación, creamos la máquina virtual especificando el grupo de recursos, el usuario de dicha máquina, la imagen de SO que queremos y la utilización de clave SSH.

~~~
# Crear la máquina virtual
$ az vm create --resource-group myResourceGroup-francecentral --admin-username gemazure-francecentral --name ubuntuFranceCentral --location francecentral --image Canonical:UbuntuServer:18.04-LTS:18.04.201812060 --generate-ssh-keys
~~~

<p align="center">
  <img width="550" height="230" src="images/hito 4/mv-francecentral.png">
</p>

Para poder abrir y hacer uso del puerto 80, debemos ejecutar la siguiente línea:

~~~
$ az vm open-port --port 80 --resource-group myResourceGroup-francecentral --name ubuntuFranceCentral
~~~

Por último, debemos poner que la IP sea estática, para que no varíe cada vez que se inicie la máquina. Y con esto, ya podemos medir las prestaciones de la máquina. Para ello, provisionamos la máquina virtual con los requerimientos de nuestra aplicación, accedemos mediante SSH a la máquina virtual, lanzamos la aplicación y desde nuestra consola local ejecutamos algunas de las herramientas de medición de prestaciones como `httperf` o `ab`.

#### Medición de prestaciones con httperf <a name="id4"></a>

Para hacer uso de la [herramienta httperf](http://www.mervine.net/performance-testing-with-httperf), usamos la siguiente ejecución:

~~~
$ httperf --server 40.89.154.66 --port 80 --num-conns 10 --rate 1
~~~

<p align="center">
  <img width="600" height="240" src="images/hito 4/httperf-francecentral.png">
</p>

En este ejemplo, se están ejecutando diez conexiones [`--num-conns 10`] a través de 40.89.154.66 [`--server 40.89.154.66`] a una velocidad de una conexión por segundo [`--rate 1`]. Me centro en las siguientes salidas:

- _Connection rate_: es la tasa de conexión.
- _Connection time [ms]_: es el tiempo de conexión.
- _Reply size_: es el tamaño de la respuesta.
- _Reply status_: es el estado de la respuesta, asegurarse que está orientado al 200.

#### Medición de prestaciones con ab <a name="id5"></a>

Para hacer uso de la [herramienta ab](https://www.petefreitag.com/item/689.cfm), usamos la siguiente ejecución, en la cual se indica con `-n` el número de peticiones a ejecutar en el benchmarck y con `-c` el número máximo de peticiones que se podrán ejecutar simultáneamente. En nuestro caso serán 10 peticiones múltiples al mismo tiempo hechas a nuestro servidor y 100 peticiones a ejecutar:

~~~
$ ab -n 100 -c 10 http://40.89.154.66/
~~~

<p align="center">
  <img width="650" height="450" src="images/hito 4/ab-francecentral.png">
</p>


### Crear máquina virtual con Ubuntu Server 18.04 LTS en el centro de datos del sur de Francia <a name="id6"></a>

Para la creación de la misma máquina máquina virtual en el centro de datos del sur de Francia, realizamos el mismo procedimiento que para el anterior centro de datos. Sin embargo, cuando intentamos crearnos dicho recurso, nos dice que dicha localización no está disponible.

<p align="center">
  <img width="850" height="40" src="images/hito 4/error-francesouth.png">
</p>

Como no es posible crearse un recurso en ese centro de datos, pasamos al siguiente centro de datos más cercano, correspondiente con el oeste de Reino Unido.

### Crear máquina virtual con Ubuntu Server 18.04 LTS en el centro de datos del oeste de Reino Unido <a name="id7"></a>

Para la creación de la misma máquina máquina virtual en el centro de datos del oeste de Reino Unido, realizamos el mismo procedimiento que para el anterior centro de datos.

~~~
# Crear el grupo de recursos
$ az group create --name myResourceGroup-ukwest --location ukwest

# Crear la máquina virtual
$ az vm create --resource-group myResourceGroup-ukwest --admin-username gemazure-ukwest --name ubuntuUKWest --location ukwest --image Canonical:UbuntuServer:18.04-LTS:18.04.201812060

# Abrir y usar el puerto 80
$ az vm open-port --port 80 --resource-group myResourceGroup-ukwest --name ubuntuUKWest
~~~

<p align="center">
  <img width="550" height="230" src="images/hito 4/mv-ukwest.png">
</p>

#### Medición de prestaciones con httperf <a name="id8"></a>

Para hacer uso de la [herramienta httperf](http://www.mervine.net/performance-testing-with-httperf), usamos la siguiente ejecución, centrándonos en los mismos valores comentados anteriormente:

~~~
$ httperf --server 51.140.226.194 --port 80 --num-conns 10 --rate 1
~~~

<p align="center">
  <img width="600" height="240" src="images/hito 4/httperf-ukwest.png">
</p>


#### Medición de prestaciones con ab <a name="id9"></a>

Para hacer uso de la [herramienta ab](https://www.petefreitag.com/item/689.cfm), usamos la siguiente ejecución, expplicada anteriormente:

~~~
$ ab -n 100 -c 10 http://51.140.226.194/
~~~

<p align="center">
  <img width="650" height="450" src="images/hito 4/ab-ukwest.png">
</p>



### Crear máquina virtual con Ubuntu Server 18.04 LTS en el centro de datos del norte de Europa <a name="id10"></a>

Para la creación de la misma máquina máquina virtual en el centro de datos del oeste de Reino Unido, realizamos el mismo procedimiento que para el anterior centro de datos.

~~~
# Crear el grupo de recursos
$ az group create --name myResourceGroup-northeurope --location northeurope

# Crear la máquina virtual
$ az vm create --resource-group myResourceGroup-northeurope --admin-username gemazure-northeurope --name ubuntuNorthEurope --location northeurope --image Canonical:UbuntuServer:18.04-LTS:18.04.201812060

# Abrir y usar el puerto 80
$ az vm open-port --port 80 --resource-group myResourceGroup-northeurope --name ubuntuNorthEurope
~~~

<p align="center">
  <img width="550" height="230" src="images/hito 4/mv-northeurope.png">
</p>

#### Medición de prestaciones con httperf <a name="id11"></a>

Para hacer uso de la [herramienta httperf](http://www.mervine.net/performance-testing-with-httperf), usamos la siguiente ejecución, centrándonos en los mismos valores comentados anteriormente:

~~~
$ httperf --server 104.41.221.120 --port 80 --num-conns 10 --rate 1
~~~

<p align="center">
  <img width="600" height="240" src="images/hito 4/httperf-northeurope.png">
</p>

#### Medición de prestaciones con ab <a name="id12"></a>

Para hacer uso de la [herramienta ab](https://www.petefreitag.com/item/689.cfm), usamos la siguiente ejecución, expplicada anteriormente:

~~~
$ ab -n 100 -c 10 http://104.41.221.120/
~~~

<p align="center">
  <img width="650" height="450" src="images/hito 4/ab-northeurope.png">
</p>


### Tabla comparativa de mediciones con httperf <a name="id13"></a>

Como se aprecia en la tabla, obtenemos una respuesta más rápida (menos tiempo) con el centro de datos ubicado en el centro de Francia. Esto es lógico, porque de los tres centros de datos, ese es el más cercano a mi ubicación.

|  | Centro de Francia | Oeste de Reino Unido | Norte de Europa |
|-----------------------------|-------------------|----------------------|-----------------|
| Connection rate [ms/conn] | 907.7 | 910.8 | 911.9 |
| Connection time [ms] | 36.2 | 50.5 | 55.5 |
| Reply time in response [ms] | 35.7 | 51.0 | 55.2 |
| Reply time in transfer [ms] | 0.4 | 0.4 | 0.4 |

### Tabla comparativa de mediciones con ab <a name="id14"></a>

Para el centro de datos del centro de Francia, en donde el test para 100 peticiones con una concurrencia de 10, ha terminado correctamente en un tiempo de 0.776 segundos (menor que para el resto de centro de datos). Se ha tardado 77.615  milisegundos para cada petición y una media de 7.761 si tenemos en cuenta la concurrencia. Obteniendo los mejores resultados. Esto es lógico, porque de los tres centros de datos, ese es el más cercano a mi ubicación.

|  | Centro de Francia | Oeste de Reino Unido | Norte de Europa |
|--------------------------------------------------------------|-------------------|----------------------|-----------------|
| Time taken for tests [seconds] | 0.776 | 1.044 | 1.169 |
| Time per request (mean) [ms] | 77.615 | 104.371 | 116.899 |
| Time per request (mean, across all concurrent requests) [ms] | 7.761 | 10.437 | 11.690 |

**Por tanto, podemos concluir que el centro de datos ubicado en el centro de Francia es el mejor según nuestras condiciones.** Y con ello, podemos dar paso a la creación del script de aprovisionamiento ([enlace](https://github.com/Gecofer/proyecto-CC/blob/master/docs/acopio.md)).


[2]: https://www.fullstackpython.com/operating-systems.html
[3]: https://www.stackscale.es/ubuntu-16-04-lts/
[4]: https://maslinux.es/ya-tenemos-ubuntu-18-04-lts-te-presentamos-todas-las-novedades/
[5]: https://www.quora.com/What-is-best-production-server-for-Flask-apps-Ubuntu-or-CentOS
[6]: https://www.dagorret.com.ar/actualizar-ubuntu-16-04-lts-server-ubuntu-18-04-lts-beta/
[7]: https://www.dagorret.com.ar/actualizar-ubuntu-16-04-lts-server-ubuntu-18-04-lts-beta/
[8]: https://docs.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-list-locations
[9]: https://www.tutiempo.net/calcular-distancias.html
[10]: https://www.internetya.co/servidores-dedicados-linux-centos-o-ubuntu/
[11]: https://www.digitalocean.com/community/questions/whats-is-better-and-why-linux-centos-or-ubuntu
