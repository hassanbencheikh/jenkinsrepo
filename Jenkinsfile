pipeline {
    // We still need a top-level agent, but it will just coordinate.
    agent any

    environment {
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'python-devsecops-jenkins_app'
        // This image has Docker-Compose and Trivy pre-installed
        // This is much cleaner than installing it yourself.
        BUILD_TOOLS_IMAGE = 'docker/compose:latest' 
        TRIVY_IMAGE = 'aquasec/trivy:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm [cite: 2]
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
                        sh 'python3 -m venv venv' [cite: 3]
                        sh './venv/bin/pip install -r requirements.txt'
                    }
                }
                stage('Run Tests') {
                    steps {
                        sh './venv/bin/pytest' [cite: 4]
                    }
                }
                stage('Static Code Analysis (Bandit)') {
                    steps {
                        sh './venv/bin/bandit -r .' [cite: 6]
                    }
                }
                stage('Check Dependency Vulnerabilities (Safety)') {
                    steps {
                        sh './venv/bin/safety check' [cite: 9]
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
                sh 'docker-compose build' [cite: 10]
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
                sh 'trivy image ${IMAGE_NAME}:latest' [cite: 7]
            }
        }

        stage('Deploy Application') {
            agent {
                docker { image env.BUILD_TOOLS_IMAGE }
            }
            steps {
                sh 'docker-compose up -d' [cite: 11]
            }
        }
    }

    // --- Post-build actions ---
    post {
        always {
            // We use a docker-compose agent to ensure we can
            // always run 'docker-compose down'
            agent {
                docker { image env.BUILD_TOOLS_IMAGE }
            }
            steps {
                echo "Cleaning up containers..."
                sh 'docker-compose down' // Bring down the deployed app
                cleanWs() [cite: 12] // Cleans the Jenkins workspace
            }
        }
    }
}
