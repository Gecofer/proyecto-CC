# Creación de una misma máquina virtual en distintos centros de datos <a name="id6"></a>

**Tabla de Contenidos**
- [Elección del sistema operativo](#id0)
- [Elección del centro de datos](#id1)


## Elección del sistema operativo <a name="id0"></a>

Antes de empezar con la creación de las máquinas virtuales en distintos centros de datos, vamos a detenernos un momento y pensar que tipo de SO nos conviene para nuestro proyecto, en el cual se hace uso [Python](https://www.python.org) y del [Flask](http://flask.pocoo.org). Afortunadamente, la comunidad de código abierto provee Linux al mundo Python como un sistema operativo libre y sólido para ejecutar nuestras aplicaciones [[2][2]]. Los únicos sistemas operativos recomendados para la producción de implementaciones en Python son Linux y FreeBSD: las versiones de Ubuntu Long Term Support (LTS), Red Hat Enterprise Linux y CentOS son opciones viables. Veamos que características nos aporta cada una de ellas:

- **Ubuntu Long Term Support (LTS)**: son las versiones recomendadas para las implementaciones, ya que reciben cinco años de actualizaciones posteriores a su publicación. Además, de que cada dos años, Canonical crea una nueva versión de LTS, lo que permite una fácil ruta de actualización, así como flexibilidad para saltarse cualquier otra versión de LTS si es necesario. A partir de mayo de 2018, 18.04 Bionic Beaver es la última versión de Ubuntu LTS. Xenial Xerus incluye Python 3.6 como su versión predeterminada de Python, que es una actualización importante en comparación con la 2.7 en Ubuntu 14.04 LTS y una sólida mejora sobre Python 3.5 incluida en Ubuntu 16.04 LTS. A continuación, enumeramos las últimas tres versiones LTS:

  - Ubuntu 14.04 LTS trae por defecto la versión de Python 2.7.6 y 3.4.0 [[2][2]]
  - Ubuntu 16.04 LTS trae por defecto la versión de Python 2.7 y 3.5 [[3][3]]
  - Ubuntu 18.04 LTS trae por defecto la versión de Python 2.7 y 3.6 [[4][4]]


- **Red Hat Enterprise Linux (RHEL)** y **Community ENTerprise Operating System (CentOS)** son la misma distribución. La principal diferencia entre los dos es que CentOS es un derivado libre de RHEL de código abierto y con licencias liberales. Además, utilizan un gestor de paquetes y una interfaz de línea de comandos diferentes de las distribuciones de Linux basadas en Debian: RPM Package Manager (RPM) y el Yellowdog Updater, Modified (YUM).

Es por ello que voy hacer uso de una versión LTS de Ubuntu para mi proyecto, debido a la estabilidad, y la instalación predefinida de Python tanto para la versión 2 como 3. Ya que CentOS 7 incluye python 2.7 pero sólo se actualiza con versiones de puntos que pueden causar problemas con algunos módulos de Python, y es necesario para los servicios del sistema, por lo que el procedimiento estándar es instalar una segunda versión en _/opt_ para usar en aplicaciones [[5][5]]. Además, en el hito anterior, se llevó a cabo el provisionamiento tanto en Ubuntu como en CentOS, lo que sirvió para comprender los problemas de las versiones de Python en CentOS, explicados anteriormente. Además, en el siguiente [enlace](https://www.quora.com/What-is-best-production-server-for-Flask-apps-Ubuntu-or-CentOS) se nos recomienda que usemos Ubuntu LTS en aplicaciones a usar Flask.

Sin embargo, una vez elegido el Ubuntu Server LTS como sistema operativo, vamos a ver que versión escoger de dicho SO. A continuación, se ven los ciclos de vida de las versiones de Ubuntu [[6][6]]:

<p align="center">
  <img width="550" height="260" src="images/hito 4/ciclo-ubuntu.png">
</p>

Como podemos comprobar, la versión 14.04 LTS termina su mantenimiento en 2019, esto puede suponer un problema si la asignatura se alarga durante ese año. Es por eso que descartamos la versión 14.04. Por otro lado, tanto las versiones 16.04 como 18.04, disponen de más años de mantenimiento. Sin embargo, el tiempo de soporte de Ubuntu 18.04 se ha aumentado de 5 a 10 años, punto a favor sobre esa versión [[7][7]]. Además, la última versión de Python estable es la 3.6 y dicha versión viene instalada por defecto en la 18.04 LTS.

**Por tanto, podemos confirmar que el mejor SO para nuestro proyecto es la versión de Ubuntu Server 18.04 LTS.**


## Elección del centro de datos <a name="id1"></a>

Para escoger el centro de datos, en el cual desplegar nuestra aplicación, vamos a obtener las mediciones de velocidad de las máquinas virtuales creadas con las mismas prestaciones, haciendo uso de herramientas como `ab` o `httperf`. Lo primero que tenemos que saber son los [centros de datos de los que dispone Azure](https://azure.microsoft.com/es-es/global-infrastructure/regions/) [[8][8]].

<!---
![](capturas/regiones-azure.png)

~~~
# Listar las regiones admitidas para la suscripción actual
$ az account list-locations
~~~

_**Pincha [aquí]() para ver la lista completa.**_

Por lógica, debemos buscar un centro de datos cercano a nuestra ubicación actual, es por ello, que nos quedamos con los centros de datos disponibles en Europa:

- **Centro de Francia** (_francecentral_), ubicado en latitud 46.3772 y longitud 2.3730
- **Sur de Francia** (_francesouth_), ubicado en latitud 43.8345 y longitud 2.1972
- **Sur de Reino Unido** (_uksouth_), ubicado en latitud 50.941 y longitud -0.799
- **Oeste de Reino Unido** (_ukwest_), ubicado en latitud 53.427 y longitud -3.084
- **Norte de Europa** (_northeurope_), ubicado en latitud 53.3478 y longitud -6.2597
- **Oeste de Europa** (_westeurope_), ubicado en latitud 52.3667 y longitud 4.9

Debido a que la creación de recursos como de máquinas virtuales, consumen dinero, solo nos vamos a quedar con las tres localizaciones más cercanas a Granada (latitud: 37.1886273, longitud: -3.5907775) [[9][9]].

- Distancia de Granada al Centro de Francia: 1135.36 km
- Distancia de Granada al Sur de Francia: 886.62 km
- Distancia de Granada al Sur de Reino Unido: 1546.57 km
- Distancia de Granada al Oeste de Reino Unido: 1807.79
- Distancia de Granada al Norte de Europa: 1810.33 km
- Distancia de Granada al Oeste de Europa: 1814.68 km

Por tanto, se van a comprobar los centros de datos del **Centro de Francia**, **Sur de Francia** y **Sur de Reino Unido**, para nuestra aplicación.

###### Creación de una máquina virtual con Ubuntu Server 18.06 LTS en el centro de datos del centro de Francia

~~~
# Listar las máquinas virtuales con localización en el centro de Francia con Ubuntu Server
$ az vm image list-skus --location francecentral --publisher Canonical --offer UbuntuServer --output table
~~~

![](capturas/lista-Ubuntu-francecentral.png)

~~~
# Listar las máquinas virtuales con localización en el centro de Francia con Ubuntu Server 18.04 LTS
$ az vm image list --location francecentral --publisher Canonical --offer UbuntuServer --sku 18.04-LTS --all --output table
~~~

![](capturas/lista-Ubuntu1804-francecentral.png)

~~~
# Visualizar la información sobre una máquina virtual en concreto
$ az vm image show --location francecentral --urn Canonical:UbuntuServer:18.04-LTS:18.04.201812060
~~~

![](capturas/informacion-Ubuntu-concreta.png)

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

![](capturas/mv-francecentral.png)

Para poder hacer uso del puerto 80, debemos ejecutar la siguiente línea:

~~~
$ az vm open-port --port 80 --resource-group myResourceGroup-francecentral --name ubuntuFranceCentral
~~~

Por último, debemos poner que la IP sea estática, para que no varíe cada vez que se inicie la máquina. Y con esto, ya podemos medir las prestaciones de la máquina. Para ello, provisionamos la máquina virtual con los requerimientos de nuestra aplicación, accedemos mediante SSH a la máquina virtual, lanzamos la aplicación y desde nuestra consola local ejecutamos algunas de las herramientas de medición de prestaciones como `httperf` o `ab`.

_**Medición de prestaciones con httperf**_

Para hacer uso de la [herramienta httperf](http://www.mervine.net/performance-testing-with-httperf), usamos la siguiente ejecución:

~~~
$ httperf --server 40.89.154.66 --port 80 --num-conns 10 --rate 1
~~~

![](capturas/httperf-francecentral.png)

En este ejemplo, se están ejecutando diez conexiones[`--num-conns 10`] a través de mervine.net[`--server 40.89.154.66`] a una velocidad de una conexión por segundo[`--rate 1`]. Y me centro en las siguientes salidas:

- _Connection rate_: es la tasa de conexión.
- _Connection time [ms]_: es el tiempo de conexión.
- _Reply size_: es el tamaño de la respuesta.
- _Reply status_: es el estado de la respuesta, asegurarse que está orientado al 200.

_**Medición de prestaciones con ab**_


Para hacer uso de la [herramienta ab](https://www.petefreitag.com/item/689.cfm), usamos la siguiente ejecución:

~~~
$ ab -n 100 -c 10 http://40.89.154.66/
~~~

![](capturas/ab-francecentral.png)



###### Creación de una máquina virtual con Ubuntu Server 18.06 LTS en el centro de datos del sur de Francia

Una vez, que tenemos decidida nuestra máquina virtual, vamos a proceder a crearla. Para ello, lo primero que haremos será crear el grupo de recursos para indicar el centro de datos en el que se va a alojar, en este caso en el sur de Francia.

~~~
# Crear el grupo de recursos
$ az group create --name myResourceGroup-francesouth --location francesouth
~~~

A continuación, creamos la máquina virtual especificando el grupo de recursos, el usuario de dicha máquina, la imagen de SO que queremos y la utilización de clave SSH.


![](capturas/error-francesouth.png)

Como no es posible crearse un recurso en ese centro de datos, pasamos al siguiente centro de datos más cercano, que es el sur de Reino Unido.

###### Creación de una máquina virtual con Ubuntu Server 18.06 LTS en el centro de datos del sur de Reino Unido

~~~
# Listar las máquinas virtuales con localización en el sur de Reino Unido con Ubuntu Server
$ az vm image list-skus --location uksouth --publisher Canonical --offer UbuntuServer --output table
~~~

![](capturas/lista-Ubuntu-uksouth.png)

~~~
# Listar las máquinas virtuales con localización en el sur de Reino Unido con Ubuntu Server 18.04 LTS
$ az vm image list --location uksouth --publisher Canonical --offer UbuntuServer --sku 18.04-LTS --all --output table
~~~

![](capturas/lista-Ubuntu1804-uksouth.png)

- **Centro de Francia** (_francecentral_), ubicado en latitud 46.3772 y longitud 2.3730
- **Sur de Francia** (_francesouth_), ubicado en latitud 43.8345 y longitud 2.1972
- **Sur de Reino Unido** (_uksouth_), ubicado en latitud 50.941 y longitud -0.799
- **Oeste de Reino Unido** (_ukwest_), ubicado en latitud 53.427 y longitud -3.084
- **Norte de Europa** (_northeurope_), ubicado en latitud 53.3478 y longitud -6.2597
- **Oeste de Europa** (_westeurope_), ubicado en latitud 52.3667 y longitud 4.9


~~~
# Visualizar la información sobre una máquina virtual en concreto
$ az vm image show --location uksouth --urn Canonical:UbuntuServer:18.04-LTS:18.04.201812060
~~~

-----

Una vez, que tenemos decidida nuestra máquina virtual, vamos a proceder a crearla. Para ello, lo primero que haremos será crear el grupo de recursos para indicar el centro de datos en el que se va a alojar, en este caso en el sur de Reino Unido.

~~~
# Crear el grupo de recursos
$ az group create --name myResourceGroup-ukwest --location ukwest
~~~

A continuación, creamos la máquina virtual especificando el grupo de recursos, el usuario de dicha máquina, la imagen de SO que queremos y la utilización de clave SSH.

~~~
# Crear la máquina virtual
$ az vm create --resource-group myResourceGroup-ukwest --admin-username gemazure-ukwest --name ubuntuUKWest --location ukwest --image Canonical:UbuntuServer:18.04-LTS:18.04.201812060
~~~

![](capturas/mv-ukwest.png)

Para poder hacer uso del puerto 80, debemos ejecutar la siguiente línea:

~~~
$ az vm open-port --port 80 --resource-group myResourceGroup-ukwest --name ubuntuUKWest
~~~

Por último, debemos poner que la IP sea estática, para que no varíe cada vez que se inicie la máquina. Y con esto, ya podemos medir las prestaciones de la máquina. Para ello, provisionamos la máquina virtual con los requerimientos de nuestra aplicación, accedemos mediante SSH a la máquina virtual, lanzamos la aplicación y desde nuestra consola local ejecutamos algunas de las herramientas de medición de prestaciones como `httperf` o `ab`.

_**Medición de prestaciones con httperf**_

Para hacer uso de la [herramienta httperf](http://www.mervine.net/performance-testing-with-httperf), usamos la siguiente ejecución:

~~~
$ httperf --server 51.140.226.194 --port 80 --num-conns 10 --rate 1
~~~

![](capturas/httperf-ukwest.png)

En este ejemplo, se están ejecutando diez conexiones[`--num-conns 10`] a través de 51.140.226.194[`--server 51.140.226.194`] a una velocidad de una conexión por segundo[`--rate 1`]. Y me centro en las siguientes salidas:

- _Connection rate_: es la tasa de conexión.
- _Connection time [ms]_: es el tiempo de conexión.
- _Reply size_: es el tamaño de la respuesta.
- _Reply status_: es el estado de la respuesta, asegurarse que está orientado al 200.

_**Medición de prestaciones con ab**_


Para hacer uso de la [herramienta ab](https://www.petefreitag.com/item/689.cfm), usamos la siguiente ejecución:

~~~
$ ab -n 100 -c 10 http://51.140.226.194/
~~~

![](capturas/ab-ukwest.png)


###### Creación de una máquina virtual con Ubuntu Server 18.06 LTS en el centro de datos del sur de Reino Unido

 **Norte de Europa** (_northeurope_), ubicado en latitud 53.3478 y longitud -6.2597

 Una vez, que tenemos decidida nuestra máquina virtual, vamos a proceder a crearla. Para ello, lo primero que haremos será crear el grupo de recursos para indicar el centro de datos en el que se va a alojar, en este caso en el sur de Reino Unido.

 ~~~
 # Crear el grupo de recursos
 $ az group create --name myResourceGroup-northeurope --location northeurope
 ~~~

 A continuación, creamos la máquina virtual especificando el grupo de recursos, el usuario de dicha máquina, la imagen de SO que queremos y la utilización de clave SSH.

 ~~~
 # Crear la máquina virtual
 $ az vm create --resource-group myResourceGroup-northeurope --admin-username gemazure-northeurope --name ubuntuNorthEurope --location northeurope --image Canonical:UbuntuServer:18.04-LTS:18.04.201812060
 ~~~

 ![](capturas/mv-northeurope.png)

 Para poder hacer uso del puerto 80, debemos ejecutar la siguiente línea:

 ~~~
 $ az vm open-port --port 80 --resource-group myResourceGroup-northeurope --name ubuntuNorthEurope
 ~~~

 Por último, debemos poner que la IP sea estática, para que no varíe cada vez que se inicie la máquina. Y con esto, ya podemos medir las prestaciones de la máquina. Para ello, provisionamos la máquina virtual con los requerimientos de nuestra aplicación, accedemos mediante SSH a la máquina virtual, lanzamos la aplicación y desde nuestra consola local ejecutamos algunas de las herramientas de medición de prestaciones como `httperf` o `ab`.

 _**Medición de prestaciones con httperf**_

 Para hacer uso de la [herramienta httperf](http://www.mervine.net/performance-testing-with-httperf), usamos la siguiente ejecución:

 ~~~
 $ httperf --server 104.41.221.120 --port 80 --num-conns 10 --rate 1
 ~~~

 ![](capturas/httperf-northeurope.png)

 En este ejemplo, se están ejecutando diez conexiones[`--num-conns 10`] a través de 51.140.226.194[`--server 51.140.226.194`] a una velocidad de una conexión por segundo[`--rate 1`]. Y me centro en las siguientes salidas:

 - _Connection rate_: es la tasa de conexión.
 - _Connection time [ms]_: es el tiempo de conexión.
 - _Reply size_: es el tamaño de la respuesta.
 - _Reply status_: es el estado de la respuesta, asegurarse que está orientado al 200.

 _**Medición de prestaciones con ab**_


 Para hacer uso de la [herramienta ab](https://www.petefreitag.com/item/689.cfm), usamos la siguiente ejecución:

 ~~~
 $ ab -n 100 -c 10 http://104.41.221.120/
 ~~~

![](capturas/ab-northeurope.png)

---->
[2]: https://www.fullstackpython.com/operating-systems.html
[3]: https://www.stackscale.es/ubuntu-16-04-lts/
[4]: https://maslinux.es/ya-tenemos-ubuntu-18-04-lts-te-presentamos-todas-las-novedades/
[5]: https://www.quora.com/What-is-best-production-server-for-Flask-apps-Ubuntu-or-CentOS
[6]: https://www.dagorret.com.ar/actualizar-ubuntu-16-04-lts-server-ubuntu-18-04-lts-beta/
[7]: https://www.dagorret.com.ar/actualizar-ubuntu-16-04-lts-server-ubuntu-18-04-lts-beta/
[8]: https://docs.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-list-locations
[9]: https://www.tutiempo.net/calcular-distancias.html
