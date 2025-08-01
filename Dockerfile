# 1.  une image officielle de Python
FROM python:3.12-slim

# 2. Définir le répertoire de travail dans le conteneur
WORKDIR /app

# 3. Copier les fichiers du projet dans l’image Docker
COPY . /app

# 4. Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat \
    && apt-get clean

# 5. Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Collecter les fichiers statiques (pour prod)
RUN python manage.py collectstatic --noinput

# 7. Exposer le port sur lequel le conteneur va tourner
EXPOSE 8000

# 8. Commande de démarrage avec gunicorn
CMD ["gunicorn", "tickets_managements.wsgi:application", "--bind", "0.0.0.0:8000"]
