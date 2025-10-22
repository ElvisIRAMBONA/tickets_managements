FROM python:3.12-slim

WORKDIR /app

# Copier uniquement ce qui est nécessaire pour installer les dépendances
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir --timeout=300 --retries=10 -r requirements.txt

# Copier le reste du projet
COPY . /app

# Exposer le port Django
EXPOSE 8000

# Commande par défaut pour lancer le serveur
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
