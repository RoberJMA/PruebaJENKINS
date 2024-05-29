Accede al contenedor de Jenkins:

    docker exec -it jenkins bash

Instalar ssh 

    apt-get update && apt-get install -y openssh-client sshpass
    

Cambia al usuario jenkins:

    su jenkins

Crea el directorio .ssh si no existe y establece los permisos correctos:

    mkdir -p /var/jenkins_home/.ssh
    chmod 700 /var/jenkins_home/.ssh

Genera la clave SSH:

    ssh-keygen -t rsa -b 4096 -C "jenkins@docker" -f /var/jenkins_home/.ssh/id_rsa -N ""

Verifica que los archivos id_rsa y id_rsa.pub existan:
    
    ls -la /var/jenkins_home/.ssh

Deberías ver algo como esto:

    -rw------- 1 jenkins jenkins 3243 May 25 10:00 id_rsa
    -rw-r--r-- 1 jenkins jenkins  745 May 25 10:00 id_rsa.pub

Copiar la Clave Pública al Servidor Remoto

    sshpass -p 'mi_contraseña' ssh-copy-id -i /var/jenkins_home/.ssh/id_rsa.pub usuario@ip_destino

Reemplaza 'mi_contraseña' con la contraseña real del usuario.
