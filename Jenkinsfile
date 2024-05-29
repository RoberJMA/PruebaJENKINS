pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/RoberJMA/PruebaJENKINS.git'
        REPO_DIR = 'PruebaJENKINS'
        SELENIUM_HUB_URL = 'http://192.168.56.10:31351'
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
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'cd /home/vagrant && git clone $REPO_URL && cd $REPO_DIR && mv *.sql /vagrant && cd $REPO_DIR/elk mv *.yaml /vagrant '"
                    '''
                }
            }
        }

        stage('Desplegar Kubernetes') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'cd $REPO_DIR && kubectl apply -f proyecto.yml'"
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

        stage('Desplegar Selenium Grid') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'cd $REPO_DIR && kubectl apply -f selenium/selenium.yaml'"
                    '''
                }
            }
        }

        stage('Desplegar ELK') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR && vagrant ssh controlplane -c 'kubectl apply -f /vagrant/pvc.yaml && kubectl apply -f /vagrant/kibana.yaml && kubectl apply -f /vagrant/filebeat.yaml'"
                    '''
                }
            }
        }

        stage('Verificar e instalar pytest') {
            steps {
                script {
                    // Verificar si pytest está instalado
                    def pytestInstalled = sh(script: 'dpkg -l | grep pytest', returnStatus: true)
                    // Si no está instalado, instalar pytest
                    if (pytestInstalled != 0) {
                        sh 'sudo apt update'
                        sh 'sudo apt install -y python3-pytest'
                    }
                }
            }
        }

        stage('Pruebas con Selenium') {
            steps {
                script {
                    sh '''
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR/selenium/tests && pytest test-login-selenium.py"
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR/selenium/tests && pytest test-registro-selenium.py"
                    ssh -i /var/jenkins_home/.ssh/id_rsa usuario@ip_maquina "cd $REPO_DIR/selenium/tests && pytest test-añadir-libros-selenium.py"
                    '''
                }
            }
        }
    }
}
