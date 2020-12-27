import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')


# Set project admin credentials
ADMINS = (
    (os.getenv("ADMIN_NAME"), os.getenv("ADMIN_EMAIL")),
)


MANAGERS = ADMINS


LOGIN_URL = '/admin/login/'


# SMTP server configurations
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("ADMIN_EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("ADMIN_EMAIL_PASS")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = None
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Account configurations
SIGNUP_REDIRECT = "/welcome/"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    'localhost',
]


INSTALLED_APPS = [

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'oauth2_provider',
    'rest_framework',
    'crispy_forms',

    # Local APPs
    'oauth.apps.OauthConfig',
    'account.apps.AccountConfig',
]


AUTH_USER_MODEL = 'account.User'


OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups',
        'introspection': 'Introspect token scope',
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    )
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'lepiota.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "static"),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Set bootstrap4 for crispy forms (used in sign up and registration templates)
CRISPY_TEMPLATE_PACK = 'bootstrap4'


WSGI_APPLICATION = 'lepiota.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sso',
        'USER': os.getenv('DB_POSTGRES_USER'),
        'PASSWORD': os.getenv('DB_POSTGRES_PASS'),
        'HOST': os.getenv('DB_POSTGRES_HOST'),
        'PORT': os.getenv('DB_POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATIC_URL = '/static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'templates'),
]


FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'account/fixtures/'),
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
