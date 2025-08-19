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
                // Use the SSH Agent plugin to securely connect to the remote server
                sshagent(credentials: ['6f7c3ac0-e049-4e40-b41e-41e70fbaa734']) {
                    script {
                        // Execute deployment commands on the remote server
                        sh """
                            ssh -o StrictHostKeyChecking=no ${REMOTE_SERVER} '''
                                echo "--> Connected to remote server"
                                cd ${DEPLOY_PATH}
                                echo "--> Pulling latest changes from Git..."
                                git pull origin main
                                echo "--> Running Docker Compose..."
                                docker-compose up -d --build --no-cache
                                echo "--> Deployment complete!"
                            '''
                        """
                    }
                }
            }
        }
    }
}