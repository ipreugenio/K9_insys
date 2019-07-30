"""
Django settings for K9_insys project.

Generated by 'django-admin startproject' using Django 2.1a1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings

#import pymysql

#pymysql.install_as_MySQLdb()

from datetime import timedelta 

from celery.task.schedules import crontab
from celery.decorators import periodic_task


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w8%l_bd@fig@3pk)zu$^!xo0tebv)t-p7!xdyz5*9cyrd-!@1e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [

    'profiles',
    'planningandacquiring',
    'deployment',
    'training',
    'unitmanagement',
    'inventory',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django.contrib.gis',
    'widget_tweaks',
    'rest_framework',

    # 'rest_framework.authtoken',

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'K9_insys.urls'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'django.template.context_processors.request'
            ],
        },
    },
]

# TEMPLATE_CONTEXT_PROCESSORS = [
#     "django.template.context_processors.request"
# ]

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)

WSGI_APPLICATION = 'K9_insys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'k9_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_IMPORTS = ('K9_insys', 'unitmanagement')
CELERY_RESULT_BACKEND = 'db+mysql://root:@localhost/k9_db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Manila'
CELER_IGNORE_RESULT = False

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators


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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Asia/Manila'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

#OTHERS SETTINGS
# if os.name == 'nt':
#     import platform
#     OSGEO4W = r"C:\OSGeo4W"
#     if '64' in platform.architecture()[0]:
#         OSGEO4W += "64"
#     assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
#     os.environ['OSGEO4W_ROOT'] = OSGEO4W
#     os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
#     os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
#     os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']


#IAN SETTINGS
if os.name == 'nt':
    import platform
    OSGEO4W = r"C:\Users\Ian Eugenio\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\osgeo"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['PATH'] = OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\data\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\data\proj"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'profiles/media')

STATICFILES_DIRS=[
    'static'
]

#LOGIN_URL = 'account/login/'
LOGIN_REDIRECT_URL = '../home/'
#SESSION_COOKIE_SECURE = False


