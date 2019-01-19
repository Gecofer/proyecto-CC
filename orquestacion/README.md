# Orquestación con Vagrant

En este hito se trata de usar `Vagrant` para provisionar una o preferiblemente varias máquinas virtuales usando un proveedor de servicios cloud, en este caso se ha usado Azure.

**Tabla de Contenidos**

- [Comprobando la instalación Vagrant](#id0)
- [Comprobando la instalación CLI de Azure](#id1)
- [Integración de Vagrant con Azure](#id2)
  - [Crear una aplicación de Azure Active Directory (AAD)](#id3)
  - [Creación del archivo Vagrantfile](#id4)


## Comprobando la instalación Vagrant <a name="id0"></a>

Lo primero que tenemos que hacer es comprobar que Vagrant está instalado, para ello hacer `vagrant --version`. Si este no es el caso dirigirse al siguiente [enlace](https://github.com/Gecofer/proyecto-CC/tree/master/provision/vagrant-ubuntu) en donde explico la instalación de Vagrant para provisionar una máquina virtual de manera local. En mi caso, dispongo de la versión 2.2.1.

~~~
$ vagrant --version
Vagrant 2.2.1
~~~

## Comprobando la instalación CLI de Azure <a name="id1"></a>

El segundo paso a realizar, es comprobar que está instalado la CLI de Azure. Debido a que Azure nos permite la creación de máquinas virtuales desde el panel de control, pero también desde la línea de órdenes. En nuestro caso, haremos uso de la línea de órdenes, para ello, lo primero que tenemos que hacer es instalarlo. Para la plataforma macOS, se puede instalar la CLI de Azure mediante el administrador de paquetes de Homebrew (se puede ver el proceso en el siguiente [enlace](https://github.com/Gecofer/proyecto-CC/blob/master/docs/automatizar-creacion-mv.md#id2)):

~~~
# Actualizar la información del repositorio de Homebrew
$ brew update

# Instalar la CLI de Azure
$ brew install azure-cli
~~~

Ya solo nos queda comprobar que la instalación ha sido un éxito con `az --version`. En mi caso, dispongo de la versión 2.0.52.

~~~
$ az --version
azure-cli (2.0.52)

...

Python location '/Library/Frameworks/Python.framework/Versions/3.6/bin/python3'
Extensions directory '/Users/gema/.azure/cliextensions'

Python (Darwin) 3.6.7 (v3.6.7:6ec5cf24b7, Oct 20 2018, 03:02:14)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]

Legal docs and information: aka.ms/AzureCliLegal
~~~

Una vez instalado, pasamos al inicio de sesión (`az login`), todo este proceso está explicado en este [enlace](https://github.com/Gecofer/proyecto-CC/blob/master/docs/automatizar-creacion-mv.md#id4).


## Integración de Vagrant con Azure <a name="id2"></a>

Una vez que tenemos en nuestra máquina Vagrant y Azure CLI, ya podemos pasar a realizar la integración de Vagrant con Azure. Para ello, tenemos que instalar **Vagrant Azure Provider**, el cual es un plugin de Vagrant que añade el proveedor Microsoft Azure a Vagrant, permitiendo así a Vagrant controlar y aprovisionar máquinas en Azure. Para la realización de este proceso, se ha seguido el siguiente [tutorial](https://github.com/Azure/vagrant-azure):

### Crear una aplicación de Azure Active Directory (AAD) <a name="id3"></a>

AAD es una combinación de aplicación/servicio principal que proporciona una identidad de servicio para que Vagrant administre nuestra suscripción a Azure. Así que, una vez instalado Azure CLI e iniciado sesión:

1. Creamos una aplicación de Azure Active Directory con acceso a Azure Resource Manager para la suscripción actual a Azure. Con el fin de obtener los siguientes datos que usaremos más adelante:
~~~
$ az ad sp create-for-rbac
~~~

  ![](../docs/images/hito5/azure1.png)

  Los valores `tenant`, `appId` y `password` se asignan a los valores de configuración `azure.tenant_id`, `azure.client_id` y `azure.client_secret` en el archivo Vagrantfile o por variables de entorno. En mi caso, voy hacer uso de variables de entorno para exportar los datos obtenidos previamente, con el fin de obtener más seguridad.

  ~~~
  $ export AZURE_TENANT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
  $ export AZURE_SUBSCRIPTION_ID=xxxxxxxxxxxxxxxxxxxxxxxxx
  $ export AZURE_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxx
  $ export AZURE_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxx
  ~~~

2. Obtenemos el identificador de la suscripción a Azure con:
~~~
$ az account list --query "[?isDefault].id" -o tsv
~~~

### Creación de Vagrantfile <a name="id4"></a>

Nos creamos una carpeta llamada orquestación, accedemos a ella y nos instalamos

~~~
$ mkdir orquestacion
$ cd orquestacion
~~~


Tal y como dice el GitHub oficial del plugin de Azure para Vagrant para configurar este dentro del Vagrantfile antes tenemos que instalar el plugin de Azure en Vagrant. Para ello ejecutaremos los siguienes comandos:

~~~
vagrant plugin install vagrant-azure
~~~

![](images/orquestacion/plugin-vagrant-azure.png)

Una vez ahí ya podemos comenzar a configurar nuestro [box](https://www.vagrantup.com/intro/getting-started/boxes.html). Desde la página de [GitHub del provider](https://github.com/Azure/vagrant-azure) se ofrece un box dummy que te dará el esqueleto del archivo Vagrantfile, que será el que describa el tipo de máquina que se va a configurar. Se debe lanzar el siguiente comando para solicitar el _box_ [[1][1]]:

~~~
$ vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box
~~~

![](images/orquestacion/azure2.png)

Ya solo nos queda obtener el archivo necesario para configurar nuestro proyecto:

~~~
$ vagrant init
~~~

![](images/orquestacion/vagrant1.png)


-----

- Explicar Vagrantfile
- Para crear en Vagrantfile poner : vagrant init

$ vagrant box add azure https://github.com/azure/vagrant-azure/raw/v2.0/dummy.box --provider azure
==> box: Box file was not detected as metadata. Adding it directly...
==> box: Adding box 'azure' (v0) for provider: azure

vagrant plugin install vagrant-azure
Installing the 'vagrant-azure' plugin. This can take a few minutes...
Installed the plugin 'vagrant-azure (2.0.0)'!

en el vagrantfile esto no
machine.vm.network "private_network", ip: "192.168.50.100", virtualbox__intnet: true

para transpasar ficheros

Quitamos clonación de ficheros

https://www.vagrantup.com/docs/provisioning/file.html


- vagrant up --no-parallel --provider=azure o require 'azure'

- los _playbook_

- Avance con la BD en mysql
