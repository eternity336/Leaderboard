pipeline {
    agent any

    environment {
        // Define the remote server user and IP address
        REMOTE_SERVER = 'jochsankehl@192.168.200.40'
        // Define the path where the repo is/will be cloned on the remote server
        DEPLOY_PATH = '/opt/jenkins/Leaderboard'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Automatically checks out the code from the Gitea repo
                checkout scm
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                sshagent(credentials: ['6f7c3ac0-e049-4e40-b41e-41e70fbaa734']) { 
                    script {
                        sh """
                            ssh -o StrictHostKeyChecking=no jochsankehl@192.168.200.40 '''
                                # Exit immediately if a command fails
                                set -e
                                echo "--> Connected to remote server"
                                cd /opt/jenkins/Leaderboard
                                echo "--> Pulling latest changes from Git..."
                                git pull origin main
                                echo "--> Stopping and removing old containers..."
                                docker-compose down
                                echo "--> Building and starting new containers..."
                                docker-compose up -d --build
                                echo "--> Deployment complete! 🚀"
                            '''
                        """
                    }
                }
            }
        }
    }
}