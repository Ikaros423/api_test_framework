pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    bat 'python -m pip install uv'
                    bat 'python -m uv sync'
                }
            }
        }
        
        stage('Run API Tests') {
            steps {
                bat 'python -m uv run pytest --junitxml=reports/report.xml --alluredir=allure-results'
            }
        }
    }
    
    post {
        always {
            junit 'reports/report.xml'

            allure([
                includeProperties: false,
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
            
            cleanWs()
        }
    }
}