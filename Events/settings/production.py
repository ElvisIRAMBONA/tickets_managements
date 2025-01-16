DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Configuration de la base de données pour la production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "events_db",
        "USER": "events_user",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    },
}


# Sécurité en production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
