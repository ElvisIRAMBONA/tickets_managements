pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'tickets-management-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DJANGO_SETTINGS_MODULE = 'Events.settings'
    }

    options {
        skipStagesAfterUnstable()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                echo '✅ Récupération du code source depuis Git...'
                checkout scm
            }
        }

        stage('Linting and Code Quality') {
            steps {
                echo '🔍 Vérification de la qualité du code...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install flake8 black isort
                    flake8 --max-line-length=88 --extend-ignore=E203,W503 apps/ apis/ Events/
                    black --check --diff apps/ apis/ Events/
                    isort --check-only --diff apps/ apis/ Events/
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🏗️ Construction de l\'image Docker...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Run Tests in Docker') {
            steps {
                echo '🧪 Exécution des tests dans Docker...'
                sh '''
                    docker run --rm -e DJANGO_SETTINGS_MODULE=Events.settings \
                        -v $(pwd)/db.sqlite3:/app/db.sqlite3 \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        sh -c "
                            python manage.py migrate &&
                            python manage.py test --verbosity=2
                        "
                '''
            }
        }

        stage('Collect Static Files') {
            steps {
                echo '📁 Collecte des fichiers statiques...'
                sh '''
                    docker run --rm -e DJANGO_SETTINGS_MODULE=Events.settings \
                        -v $(pwd)/static:/app/static \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Scan de sécurité...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install bandit
                    bandit -r apps/ apis/ Events/ -f json -o security-report.json || true
                '''
                archiveArtifacts artifacts: 'security-report.json', allowEmptyArchive: true
            }
        }

        stage('Push Docker Image') {
            steps {
                echo '📤 Push de l\'image Docker...'
                // Assumer que Docker registry est configuré (ex. : Docker Hub)
                sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                sh "docker push ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Déploiement en cours...'
                // Exemple de déploiement avec docker-compose sur un serveur distant
                // Remplacer par vos commandes de déploiement réelles
                sh '''
                    echo "Déploiement avec docker-compose..."
                    # scp docker-compose.yml user@server:/path/to/app/
                    # ssh user@server "cd /path/to/app && docker-compose pull && docker-compose up -d"
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Nettoyage...'
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
            sh 'rm -rf venv'
        }
        success {
            echo '🎉 Pipeline terminé avec succès !'
            // Notifications (ex. : Slack, Email)
            // slackSend channel: '#ci-cd', message: "Build ${env.BUILD_NUMBER} succeeded!"
        }
        failure {
            echo '❌ Le pipeline a échoué.'
            // Notifications d'échec
            // slackSend channel: '#ci-cd', message: "Build ${env.BUILD_NUMBER} failed!"
        }
    }
}
