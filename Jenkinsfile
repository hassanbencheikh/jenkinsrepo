pipeline {
    // We still need a top-level agent, but it will just coordinate.
    agent any

    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'python-devsecops-jenkins_app'
        // This image has Docker-Compose and Trivy pre-installed
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
            // This agent block applies to all stages nested inside
            agent {
                docker { image env.PYTHON_IMAGE }
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
                // Use a Docker Compose image
                docker { image env.BUILD_TOOLS_IMAGE }
            }
            steps {
                // The 'docker/compose' image's command is 'docker-compose'
                // We pass 'build' as an argument.
                sh 'docker-compose build'
            }
        }

        // --- Scan the image using a Trivy container ---
        stage('Container Vulnerability Scan (Trivy)') {
            agent {
                docker { image env.TRIVY_IMAGE }
            }
            steps {
                // The 'aquasec/trivy' image's command is 'trivy'
                // We pass 'image ...' as arguments
                sh 'trivy image ${IMAGE_NAME}:latest'
            }
        }

        stage('Deploy Application') {
            agent {
                docker { image env.BUILD_TOOLS_IMAGE }
            }
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    // --- Post-build actions ---
    post {
        always {
            // *** THIS IS THE SYNTAX FIX ***
            steps {
                agent { // We need an agent here too for docker-compose
                    docker { image env.BUILD_TOOLS_IMAGE }
                }
                echo "Cleaning up containers..."
                // Use 'try/catch' so cleanup doesn't fail the build
                // if containers are already down.
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                    sh 'docker-compose down' // Bring down the deployed app
                }
                cleanWs() //  Cleans the Jenkins workspace
            }
        }
    }
}
