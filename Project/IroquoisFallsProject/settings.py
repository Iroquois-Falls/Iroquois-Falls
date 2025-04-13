"""
Django settings for IroquoisFallsProject project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = 'static/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)2po93%_w%x3_o)56iz6%i(el5jsbj=&rys-v)7fde=2hgch(w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['iroquois-falls.azurewebsites.net']


# Application definition

INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.microsoft',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'IroquoisFalls.apps.IroquoisfallsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'IroquoisFallsProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "IroquoisFalls", "templates")],
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

WSGI_APPLICATION = 'IroquoisFallsProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'NAME': 'iroquoisfalls',  # ✅ Replace with your MySQL database name
    #    'USER': 'root',  # ✅ Replace with MySQL username
    #    'PASSWORD': 'Bym2055.',  # ✅ Replace with MySQL password
    #    'HOST': '127.0.0.1',  # ✅ Change if using a remote MySQL server
    #    'PORT': '3306',  # ✅ Default MySQL port
    #    'OPTIONS': {
    #        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
    #    }
   # }
   "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase",
}}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    "IroquoisFalls.auth_backends.CustomUserBackend",  # ✅ Uses your Users model
    "django.contrib.auth.backends.ModelBackend",  # ✅ Allows Django superuser login
]


SOCIALACCOUNT_PROVIDERS = {
    'microsoft': {
        'APP': {
            'client_id': '3be91c1b-3e01-45bd-80c9-a070a1451cfe', 
            'secret': '0ccaa186-509e-4eb3-8c86-87ebe7f5b577',  
            'key': ''
        },
        'SCOPE': ['User.Read'],
        'AUTH_PARAMS': {},
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

LOGIN_REDIRECT_URL = '/route-after-login/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/accounts/login/'  
AUTH_USER_MODEL = 'IroquoisFalls.Users'  # ✅ Use your custom Users model
SOCIAL_AUTH_MICROSOFT_REDIRECT_URI = 'http://localhost:8000/accounts/microsoft/login/callback/'
