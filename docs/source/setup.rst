Installation et Configuration
=============================

Prérequis
---------

- Python 3.12 ou supérieur
- Docker et Docker Compose
- Git

Installation des Dépendances
----------------------------

Clonez le repository et installez les dépendances Python :

.. code-block:: bash

   git clone <repository-url>
   cd tickets_managements
   pip install -r requirements.txt

Configuration de l'Environnement
---------------------------------

Créez un fichier `.env` à la racine du projet avec les variables d'environnement nécessaires (ex. : clés API, secrets).

Configuration Docker
--------------------

Le projet utilise Docker pour le déploiement. Voici la configuration :

**Dockerfile :**

.. code-block:: dockerfile

   FROM python:3.12-slim

   WORKDIR /app

   # Copier uniquement ce qui est nécessaire pour installer les dépendances
   COPY requirements.txt /app/

   # Installer les dépendances Python
   RUN pip install --no-cache-dir -r requirements.txt

   # Copier le reste du projet
   COPY . /app

   # Exposer le port Django
   EXPOSE 8000

   # Commande par défaut pour lancer le serveur
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

**docker-compose.yaml :**

.. code-block:: yaml

   services:
     web:
       build: .
       container_name: django_app
       command: >
         sh -c "
           python manage.py makemigrations &&
           python manage.py migrate &&
           python manage.py collectstatic --noinput &&
           python manage.py runserver 0.0.0.0:8000
         "
       volumes:
         - .:/app
         - ./static:/app/static
         - ./logs:/app/logs
       expose:
         - "8000"
       depends_on:
         - elasticsearch
       networks:
         - elastic-net

     nginx:
       image: nginx:alpine
       container_name: nginx_proxy
       ports:
         - "80:80"
       volumes:
         - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
         - ./static:/app/static
       depends_on:
         - web
       networks:
         - elastic-net

     elasticsearch:
       image: docker.elastic.co/elasticsearch/elasticsearch:7.17.24
       container_name: elasticsearch
       environment:
         - discovery.type=single-node
         - bootstrap.memory_lock=true
         - ES_JAVA_OPTS=-Xms512m -Xmx512m
         - xpack.security.enabled=false
         - xpack.security.transport.ssl.enabled=false
         - xpack.security.http.ssl.enabled=false
       ports:
         - "9200:9200"
       volumes:
         - esdata:/usr/share/elasticsearch/data
       networks:
         - elastic-net
       ulimits:
         memlock:
           soft: -1
           hard: -1
       restart: unless-stopped

   volumes:
     esdata:
       driver: local

   networks:
     elastic-net:
       driver: bridge

Lancement de l'Application
--------------------------

Avec Docker Compose :

.. code-block:: bash

   docker-compose up --build

L'application sera accessible sur http://localhost.

Migrations et Données Initiales
-------------------------------

Après le premier lancement, exécutez les migrations si nécessaire :

.. code-block:: bash

   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate

Configuration Nginx
-------------------

Le fichier `docker/nginx/default.conf` configure Nginx comme proxy inverse pour Django.

Déploiement en Production
-------------------------

Pour la production, assurez-vous de :

- Configurer des variables d'environnement sécurisées
- Utiliser un reverse proxy avec SSL (ex. : Let's Encrypt)
- Configurer les logs et la surveillance
- Sauvegarder la base de données et Elasticsearch régulièrement
