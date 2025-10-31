pipeline {
    agent any
    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'python-devsecops-jenkins_app'
        BUILD_TOOLS_IMAGE = 'docker/compose:latest' 
        TRIVY_IMAGE = 'aquasec/trivy:latest'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        // --- Run all Python steps inside a Python container ---
        stage('Run Python Analysis & Tests') {
            agent {
                dockerContainer { image env.PYTHON_IMAGE }
            }
            stages {
                stage('Install Dependencies') {
                    steps {
                        sh 'python3 -m venv venv'
                        sh './venv/bin/pip install -r requirements.txt'
                    }
                }
                stage('Run Tests') {
                    steps {
                        sh './venv/bin/pytest'
                    }
                }
                stage('Static Code Analysis (Bandit)') {
                    steps {
                        sh './venv/bin/bandit -r .'
                    }
                }
                stage('Check Dependency Vulnerabilities (Safety)') {
                    steps {
                        sh './venv/bin/safety check'
                    }
                }
            }
        }
        // --- Run Docker steps using Docker-Compose ---
        stage('Build Docker Image') {
            agent {
                dockerContainer { image env.BUILD_TOOLS_IMAGE }
            }
            steps {
                sh 'docker-compose build'
            }
        }
        // --- Scan the image using a Trivy container ---
        stage('Container Vulnerability Scan (Trivy)') {
            agent {
                dockerContainer { image env.TRIVY_IMAGE }
            }
            steps {
                sh 'trivy image ${IMAGE_NAME}:latest'
            }
        }
        stage('Deploy Application') {
            agent {
                dockerContainer { image env.BUILD_TOOLS_IMAGE }
            }
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
    // --- Post-build actions ---
    post {
        always {
            script {
                // Run cleanup on the main agent
                echo "Cleaning up containers..."
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                    sh 'docker-compose down'
                }
                cleanWs()
            }
        }
    }
}
