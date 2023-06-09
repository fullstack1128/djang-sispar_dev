"""
Django settings for django_regularize project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

from configurations import Configuration, values
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Dev(Configuration):
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "py*d-%9i6nitbb9jq!b5=1=@@9j!1!cb&2gf31q2z6$z8m=(5("

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = ["sispar.sjc.br", "www.sispar.sjc.br", "127.0.0.1"]

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.humanize",
        # Campo customizado de CNPJ
        "django_cpf_cnpj",
        # Crispy forms -> Para formatar formulários
        "crispy_forms",
        "crispy_bootstrap5",
        # Backend de e-mail para o Mailgun
        "anymail",
        # App do Recaptcha
        "captcha",
        # Apps locais
        "admin_regularize",
        "auth_regularize",
        "main",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "django_regularize.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "django_regularize.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases
    DATABASES = values.DatabaseURLValue(f"sqlite:///{BASE_DIR}/db.sqlite3")

    # Password validation
    # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Atualizado o algoritmo de hash da senha para o Argon2
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
        "django.contrib.auth.hashers.ScryptPasswordHasher",
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/4.1/topics/i18n/

    LANGUAGE_CODE = values.Value("pt-BR")

    TIME_ZONE = values.Value("America/Sao_Paulo")

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/

    STATIC_URL = "static/"

    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
    # Default primary key field type
    # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Modelo de usuário padrão
    AUTH_USER_MODEL = "auth_regularize.Usuario"

    # Definir se o site de admin do Django está disponível
    DJANGO_ADMIN_SITE = values.BooleanValue(True, environ_name="DJANGO_ADMIN_SITE")

    # Configurações do Crispy forms
    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

    CRISPY_TEMPLATE_PACK = "bootstrap5"

    # API SERPRO
    API_SERPRO_CONSUMER_KEY = values.Value("")

    API_SERPRO_SECRET_KEY = values.Value("")

    API_SERPRO_VERSION = values.IntegerValue(1)

    API_SERPRO_TOKEN_URL = values.Value("https://gateway.apiserpro.serpro.gov.br/token")

    SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


class Prod(Dev):
    DEBUG = True

    SECRET_KEY = "py*d-%9i6nitbb9jq!b5=1=@@9j!1!cb&2gf31q2z6$z8m=(5("


    # EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
    # MAILGUN_ACCESS_KEY = 'd30b142a4e089b3ccb5c40a02b2af088-7764770b-11d4f759'
    # MAILGUN_SERVER_NAME = 'api.mailgun.net'

    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
    ANYMAIL = {
        'MAILGUN_API_KEY': 'd30b142a4e089b3ccb5c40a02b2af088-7764770b-11d4f759',
        'MAILGUN_SENDER_DOMAIN': 'sispar.sjc.br',
    }

    # # Configurações do Backend de e-mail
    # EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    # ANYMAIL = {
    #     "MAILGUN_API_KEY": "d30b142a4e089b3ccb5c40a02b2af088-7764770b-11d4f759", #os.environ.get("DJANGO_MAILGUN_API_KEY"),
    #     "MAILGUN_API_URL": os.environ.get(
    #         "DJANGO_MAILGUN_API_URL", "https://api.mailgun.net/v3/sispar.sjc.br/messages"
    #     ),
    # }

    # DEFAULT_FROM_EMAIL = values.EmailValue()

    # Configurações Captcha
    RECAPTCHA_PUBLIC_KEY = values.Value("6LfCiv8kAAAAAIVnggo2ha72wNQgUiOHZPN7938f")

    RECAPTCHA_PRIVATE_KEY = values.Value("6LfCiv8kAAAAAEE05NQvN342YjsL2Id1TXNL3MR5")

    SILENCED_SYSTEM_CHECKS = []
