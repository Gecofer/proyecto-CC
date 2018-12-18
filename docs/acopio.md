# Script de aprovisionamiento

Para ejecutar el script haremos sh acopio.md

#!/bin/bash

# Creación del grupo de recursos con localización en el centro de Francia
#echo " ------ Creación del grupo de recursos ------ "
az group create --name myResourceGroup-francecentre --location francecentral

# Creación de la máquina virtual con Ubuntu Server 18.04 LTS, indicando el grupo
# de recursos, el usuario de dicha máquina y la generación de las clases SSH
# Además, se extrae la IP pública de la máquina y se guarda en la variable $IP
echo " ------ Creación de la máquina virtual ------ "
IP=$(az vm create --resource-group myResourceGroup-francecentre --admin-username gemazure-francecentre --name ubuntuGemaFranceCentre --location francecentral --image Canonical:UbuntuServer:18.04-LTS:18.04.201812060 --generate-ssh-keys --public-ip-address-allocation static| jq -r '.publicIpAddress')
echo " ------ Máquina virtual creada ------ "

# Una vez creada la máquina virtual, mostramos su nombre y su dirección IP
echo " ------ Datos de la máquina virtual creada ------ "
echo -name: ubuntuGemaFranceCentre
echo -ip: $IP

# Abrimos el puerto 80
echo " ------ Abrir el puerto 80 ------ "
az vm open-port --port 80 --resource-group myResourceGroup-francecentre --name ubuntuGemaFranceCentre

# Realizar provisionamiento con ansible
echo " ------ Provisionando con Ansible ------ "
ansible-playbook -i "$IP," -b provision/acopio/ansible_playbook.yml --user gemazure-francecentre -v

# Conectarnos a la máquina virtual
echo " ------ Accediendo mediante SSH a la máquina virtual ------ "
ssh gemazure-francecentre@$IP


Salida del Script
