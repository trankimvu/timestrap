import dj_database_url

from .base import *  # noqa: F401,F403


DEBUG = False


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ["SECRET_KEY"]  # noqa: F405


# SECURITY WARNING: set this to your domain name in production!

ALLOWED_HOSTS = ["*"]

# SSL

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(conn_max_age=500)}


# Channels
# https://channels.readthedocs.io/en/latest/

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [os.environ.get("REDIS_URL")]},  # noqa: F405
    }
}


# Email

SENDGRID_USERNAME = os.environ.get("SENDGRID_USERNAME", None)  # noqa: F405
SENDGRID_PASSWORD = os.environ.get("SENDGRID_PASSWORD", None)  # noqa: F405

# Use SendGrid if we have the addon installed
if SENDGRID_USERNAME and SENDGRID_PASSWORD:
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_HOST_USER = SENDGRID_USERNAME
    EMAIL_HOST_PASSWORD = SENDGRID_PASSWORD
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_ENABLED = False
