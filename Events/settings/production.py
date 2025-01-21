
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Configuration of database for production
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

sentry_sdk.init(
    dsn="https://67c99a4c972fbe1080cad8775c7b0b87@o4508676193452032.ingest.us.sentry.io/4508676201054208",
    integrations=[DjangoIntegration()],
    # Active le suivi des performances
    traces_sample_rate=1.0,
    # Active l'envoi d'informations d'environnement (utile en production)
    send_default_pii=True
)


# Security in production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
