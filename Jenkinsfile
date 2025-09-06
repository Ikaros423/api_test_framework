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
                    bat 'python3 -m pip install uv'
                    bat 'uv sync'
                }
            }
        }
        
        stage('Run API Tests') {
            steps {
                bat 'uvx pytest --junitxml=reports/report.xml --alluredir=allure-results'
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