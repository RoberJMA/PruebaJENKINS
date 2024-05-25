pipeline {
    agent any

    environment {
        REPO_URL = 'URL_DEL_REPOSITORIO' // Reemplazar con la URL del repositorio
    }

    stages {
        stage('Preparar Entorno') {
            steps {
                script {
                    // Conectarse al servidor vía SSH
                    sshagent(['id_rsa']) {
                        sh 'ssh user@remote_server'
                    }
                }
            }
        }

        stage('Clonar Repositorio') {
            steps {
                script {
                    // Clonar el repositorio en la máquina remota
                    sshagent(['id_rsa']) {
                        sh 'ssh user@remote_server "git clone $REPO_URL"'
                    }
                }
            }
        }

        stage('Levantar VMs con Vagrant') {
            steps {
                script {
                    // Levantar las máquinas virtuales con Vagrant
                    sshagent(['id_rsa']) {
                        sh 'ssh user@remote_server "cd ruta_del_repositorio && vagrant up"'
                    }
                }
            }
        }

        stage('Aprovisionar VMs con Ansible') {
            steps {
                script {
                    // Aprovisionar las máquinas virtuales con Ansible
                    sshagent(['id_rsa']) {
                        sh 'ssh user@remote_server "cd ruta_del_repositorio && ansible-playbook -i vagrant-inventory playbook.yml"'
                    }
                }
            }
        }

        stage('Desplegar Kubernetes') {
            steps {
                script {
                    // Desplegar los servicios de Kubernetes
                    sshagent(['id_rsa']) {
                        sh 'ssh user@remote_server "kubectl apply -f ruta_del_repositorio/proyecto.yml"'
                    }
                }
            }
        }

        stage('Comprobar Despliegue') {
            steps {
                script {
                    // Comprobar que todos los pods están corriendo
                    sshagent(['id_rsa']) {
                        sh 'ssh user@remote_server "kubectl get all"'
                    }
                }
            }
        }

        stage('Desplegar ELK') {
            steps {
                script {
                    // Desplegar ELK stack
                    sshagent(['id_rsa']) {
                        sh '''
                        ssh user@remote_server "kubectl apply -f ruta_del_repositorio/pvc.yaml"
                        ssh user@remote_server "kubectl apply -f ruta_del_repositorio/elastic-ss.yaml"
                        ssh user@remote_server "kubectl apply -f ruta_del_repositorio/kibana.yaml"
                        ssh user@remote_server "kubectl apply -f ruta_del_repositorio/filebeat.yaml"
                        '''
                    }
                }
            }
        }

        stage('Pruebas con Selenium') {
            steps {
                script {
                    // Ejecutar pruebas con Selenium
                    sshagent(['id_rsa']) {
                        sh 'ssh user@remote_server "cd ruta_del_repositorio/tests && pytest"'
                    }
                }
            }
        }
    }
}
