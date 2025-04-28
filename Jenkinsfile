pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    environment {
        // BOT_TOKEN = credentials('telegram-bot-token')
    }

    stages {
        stage('Initialisation') {
            steps {
                script {
                    echo "Branch name ${BRANCH_NAME}"
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    echo "Building the project..."
                    // Add your build commands here
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running tests..."
                    // Add your test commands here
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Deploying the project..."
                    // Add your deployment commands here
                }
            }
        }
    }

}