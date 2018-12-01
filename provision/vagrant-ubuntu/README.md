###### 3.1. Vagrant para crear y configurar máquinas virtuales de manera local

[Vagrant](http://www.conasa.es/blog/vagrant-la-herramienta-para-crear-entornos-de-desarrollo-reproducibles/) es una herramienta gratuita de línea de comandos, disponible para Windows, MacOS X y GNU/Linux, que permite generar entornos de desarrollo reproducibles y compartibles de forma muy sencilla. Para ello, Vagrant crea y configura máquinas virtuales a partir de simples ficheros de configuración.

- [Tutorial 1](https://fortinux.gitbooks.io/humble_tips/content/capitulo_1_usando_aplicaciones_en_linux/tutorial_instalar_vagrant_para_usar_ambientes_virtuales_en_gnulinux.html)

Para poder usar Vagrant previamente tendremos que tener instalado Virtualbox (_ver paso 1_). Una vez instalado, solo se tendrá que instalar Vagrant por línea de órdenes.

~~~
# Now install Vagrant either from the website or use homebrew for installing it
$ brew cask install vagrant
~~~

![](images/vagrant0.png)

Una vez instalado Vagrant, debemos escoger que SO vamos a usar, para ello debemos ver las funcionalidades que vamos a querer en el mismo. Es por ello, vamos a ver que servidor elegir entre Debian Server vs Ubuntu Server.

[**¿Qué es Debian y qué es Ubuntu Server?**](http://www.servidorinfo.info/que-servidor-os-elegir-en-2018-debian-server-vs-ubuntu-server/)

Ambas son versiones diferentes del sistema operativo Linux (el término para esto son distribuciones, o distribuciones para abreviar). Ubuntu Server se basa en realidad en Debian, a través de los equipos que lo ejecutan son diferentes.

_Debian_

- No ofrece actualizaciones tradicionales (donde reiniciaría el servidor para descargar e instalar la última actualización principal), sino un flujo de versiones a las que un sistema en directo puede actualizarse. Esto se puede hacer usando el administrador de paquetes apt-get, un programa que le permite instalar actualizaciones y software.

- Tiene la reputación de ser más estable.

- Tiene muchos paquetes preconfigurados (lo que significa que no necesitarán ser configurados para ejecutarse en su servidor).

_Ubuntu_

- Ubuntu tiene versiones programadas, y LTS Builds. Un LTS build es una versión de la distribución que se ofrece soporte a largo plazo (LTS). Ubuntu soporta sus versiones de LTS por un máximo de 5 años. Debian ha ofrecido normalmente sólo 3 años de soporte para sus construcciones.

- Ofrece mayor soporte que Debian.

Debido a que cada sistema operativo es gratuito, se puede elegir en función de las funciones y el soporte que se necesite. Sin embargo, hemos optado por hacer uso de Ubuntu 14.04.5 LTS, ya que viene con python3.


**¿Qué versión escoger de Debian?**

~~~
# Descargamos el SO Ubuntu 14.04:
$ vagrant box add ubuntu/trusty64 https://vagrantcloud.com/ubuntu/boxes/trusty64
~~~

![](images/vagrant1.png)

Una vez que Vagrant está instalado y ya tenemos en nuestro ordenador las cajas (boxes), vamos a crear nuestra primera máquina virtual Ubuntu. Para ello, primero creamos un directorio para ella y nos movemos allí:

~~~
$ mkdir vagrant-ubuntu
$ cd vagrant-ubuntu/

# Creamos el archivo de configuración de vagrant
$ vagrant init
~~~

![](images/vagrant2.png)

Editamos la línea `config.vm.box = "base"` por `config.vm.box = "ubuntu/trusty64"` de ese archivo, denominado Vagrantfile para que Vagrant busque el box de Ubuntu 64 que descargamos anteriormente, es decir, en ese fichero se definen las máquinas virtuales a usar. En nuestro caso, le estamos diciendo que queremos que use la máquina virtual con Ubuntu trusty de 64 bits.

~~~
$ vim Vagrantfile

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
end
~~~

Ahora, ya podemos iniciar la máquina virtual:

~~~
$ vagrant up
~~~

![](images/vagrant3.png)

Y nos conectamos a ella por ssh:

~~~
$ vagrant ssh
~~~

![](images/vagrant4.png)

~~~
# Para salir:
$ exit

# Para apagarla:
$ vagrant halt

# Para eliminar la máquina virtual:
$ vagrant destroy
~~~

Una vez que ya tenemos nuestra máquina virtual, vamos a provisionarla  vamos a conectar Ansible con Vagrant, y cuando veamos que funciona correctamente, ya podremos pasar a realizar el provisionamiento con Azure.


###### 3.3. Conectar Ansible con Vagrant y provisionar

_**Nota**: todos los archivos de vagrant y ansible tienen que estar en la misma carpeta_

**Configuración básica _ansible.cfg_**

Lo primero que tenemos que hacer es un fichero de configuración dentro de nuestro directorio. Este fichero hay que meterlo en el directorio donde estemos trabajando y básicamente le dice a Ansible que tiene que mirar en el fichero *ansible_host* (defino como se va a conectar Asnsible)

```
[defaults]
host_key_checking = False
inventory = ./ansible_hosts
```

**Inventariando los _hosts_**

En el fichero **ansible_host** se le asigna un nombre a la máquina y se configura una serie de requerimientos: cuál es el puerto SSH para acceder a la máquina virtual que hemos creado, por defecto es el 2222, y al host le estamos diciendo a la máquina que vamos acceder. Además, para acceder a la máquina virtual necesitamos una clave privada que suele estar en el directorio: *.vagrant/machines/default/virtualbox/private_key*. En general, estamos haciendo que Ansible se conecte correctamente con Vagrant mediante SSH.

```
[vagrantboxes]
ubuntuServer ansible_ssh_port=2222 ansible_ssh_host=127.0.0.1

[vagrantboxes:vars]
ansible_ssh_user=vagrant
ansible_ssh_private_key_file=.vagrant/machines/default/virtualbox/private_key
```

Ahora vamos hacer una comprobación básica (debe estar arrancada la máquina virtual), para ello hacemos un ping y vemos que tenemos acceso a ella:

```
$ ansible all -m ping
```


![](images/vagrant5.png)

Si añadimos _-v_, _-vv_ o _-vvv_ obtendremos más información, en la conexión de Ansible con Vagrant por SSH.

```
$ ansible all -m ping
```

![](images/vagrant6.png)
