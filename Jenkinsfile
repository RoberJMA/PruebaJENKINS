pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/RoberJMA/PruebaJENKINS.git'
        REPO_DIR = 'PruebaJENKINS'
        SELENIUM_HUB_URL = 'http://selenium-hub:4444/wd/hub'
    }

    stages {
        stage('Preparar Entorno') {
            steps {
                script {
                    sh 'ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina exit'
                }
            }
        }

        stage('Clonar Repositorio') {
            steps {
                script {
                    sh 'ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "git clone $REPO_URL || (cd $REPO_DIR && git pull)"'
                }
            }
        }

        stage('Levantar VMs con Vagrant') {
            steps {
                script {
                    sh 'ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant up"'
                }
            }
        }

        stage('Gestion de archivos') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'cd /home/vagrant && git clone $REPO_URL && cd $REPO_DIR && mv *.yaml /vagrant && mv *.sql /vagrant'"
                    '''
                }
            }
        }

        stage('Desplegar Kubernetes') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'kubectl apply -f /vagrant/proyecto.yml'"
                    '''
                }
            }
        }

        stage('Comprobar Despliegue') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'kubectl get all'"
                    '''
                }
            }
        }

        //No funciona correctamente -> Si lanza kubernetes pero no se agregan correctamente los nodos
        stage('Desplegar Selenium Grid') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'kubectl apply -f /vagrant/selenium-hub-deployment.yaml && kubectl apply -f /vagrant/selenium-node-chrome-deployment.yaml && kubectl apply -f /vagrant/selenium-node-firefox-deployment.yaml && kubectl apply -f /vagrant/selenium-hub-service.yaml'"
                    '''
                }
            }
        }

        //Comentado ya que consume muchos recursos-> Buen funcionamiento
        // stage('Desplegar ELK') {
        //     steps {
        //         script {
        //             sh '''
        //             ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'kubectl apply -f /vagrant/pvc.yaml && kubectl apply -f /vagrant/kibana.yaml && kubectl apply -f /vagrant/filebeat.yaml'"
        //             '''
        //         }
        //     }
        // }

        //No funciona
        //En proceso, verificar funcionamiento de Selenium por si solo primero, para adaptarlo a la aplicacion desplegada con Kubernetes
        stage('Pruebas con Selenium') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR/tests && pytest"
                    '''
                }
            }
        }
    }
}
